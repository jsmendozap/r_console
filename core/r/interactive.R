.ask_yes_no <- function(msg = NULL, default = TRUE, ...) {
    response <- send_question("ask_yes_no", list(question = msg, default = default))
    isTRUE(response$data)
}

.menu <- function(choices, graphics = FALSE, title = NULL) {
    response <- send_question("menu", list(choices = choices, title = title))
    return(response$data)
}

.file.choose <- function(new = FALSE) {
    response <- send_question("file_choose", list(new = new))
    if (is.null(response$data) || response$data == "") stop("file choice cancelled")
    return(response$data)
}

.editor <- function(name = NULL, file = NULL, title = NULL, ...) {
    if (is.null(file) || file == "") file <- name
    if (is.null(file) || file == "") return(invisible(0L))
    
    file <- normalizePath(file, mustWork = FALSE)
    if (is.null(title)) title <- basename(file)
    
    send_question("file_edit", list(file = file, title = title))
    return(invisible(0L))
}

.readline <- function(prompt = "") {
    response <- send_question("readline", list(prompt = prompt))
    if (is.null(response$data)) return("")
    return(as.character(response$data))
}

.View <- function(x, title = NULL) {
    if (missing(title)) title <- deparse(substitute(x))[1]
    
    if (is.data.frame(x) || is.matrix(x)) {
        max_rows <- 1000
        if (nrow(x) > max_rows) {
            x <- x[1:max_rows, , drop = FALSE]
            title <- paste0(title, " (Showing first ", max_rows, " rows)")
        }
        file <- tempfile(pattern = "View_", fileext = ".csv")
        write.csv(as.data.frame(x), file, row.names = FALSE)
        send_question("show_table", list(file = file, title = title))
        return(invisible(NULL))
    }
    
    file <- tempfile(pattern = "View_", fileext = ".R")
    sink(file)
    print(x)
    sink()
    .editor(file = file, title = title)
}

.patch_fn <- function(name, new_fn, pkg) {
    pkg_env <- paste0("package:", pkg)
    if (pkg_env %in% search()) {
        env <- as.environment(pkg_env)
        unlockBinding(name, env)
        assign(name, new_fn, envir = env)
        lockBinding(name, env)
    }
}

.patch_fn("menu", .menu, "utils")
.patch_fn("file.choose", .file.choose, "base")
.patch_fn("readline", .readline, "base")
.patch_fn("View", .View, "utils")

options(
    repos = c(CRAN = "https://cloud.r-project.org"),
    editor = .editor,
    rlang_interactive = TRUE,
    askYesNo = .ask_yes_no,
    browser = "false",
    shiny.launch.browser = FALSE,
    device = "pdf", 
    viewer = NULL,
    echo = FALSE, 
    max.print = 100
)