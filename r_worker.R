library(jsonlite)
library(evaluate)
options(echo = FALSE)

cat("READY\n")
flush(stdout())

.out <- stdout()

send_chunk <- function(data) {
    msg <- toJSON(list(type = "chunk", data = data), auto_unbox = TRUE)
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)
}

send_done <- function(error = NULL) {
    msg <- toJSON(
        list(type = "done", error = error, wd = getwd()),
        auto_unbox = TRUE,
        null = "null"
    )
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)
}

while (TRUE) {
    line <- readLines(con = "stdin", n = 1, warn = FALSE)
    if (length(line) == 0) break

    request <- fromJSON(line)

    if (!is.null(request$width)) {
        options(width = request$width)
    }

    error_msg <- NULL

    handler <- new_output_handler(
        text = \(x) send_chunk(x),
        value = function(x, visible) {
            if (visible) {
                text <- paste(capture.output(print(x)), collapse = "\n")
                send_chunk(paste0(text, "\n"))
            }
        },
        warning = function(x) {
            send_chunk(paste0("Warning: ", conditionMessage(x), "\n"))
            invokeRestart("muffleWarning")
        },
        error = \(x) error_msg <<- conditionMessage(x)
    )

    evaluate(request$code, output_handler = handler, stop_on_error = 1)

    send_done(error_msg)
}