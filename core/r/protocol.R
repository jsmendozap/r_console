send_chunk <- function(data) {
    msg <- toJSON(list(type = "chunk", data = data), auto_unbox = TRUE)
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)
}

send_expression <- function(expr) {
    msg <- toJSON(list(type = "expression", data = expr), auto_unbox = TRUE)
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

send_fns <- function(pkgs) {
    msg <- toJSON(list(type = "pkg", data = pkgs), auto_unbox = TRUE)
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)
}

send_help <- function(url) {
    path <- tempfile(fileext = ".html")
    tools::Rd2HTML(utils:::.getHelpFile(url), out = path)
    msg <- toJSON(list(type = "help", path = path), auto_unbox = TRUE)
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)
}

send_question <- function(method, args = NULL) {
    msg <- toJSON(
        list(type = "question", method = method, args = args),
        auto_unbox = TRUE,
        null = "null"
    )
    cat(msg, "\n", file = .out, sep = "")
    flush(.out)

    response <- fromJSON(readLines("stdin", n = 1, warn = FALSE))
    return(response)
}