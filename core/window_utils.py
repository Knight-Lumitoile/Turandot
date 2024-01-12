def center_window(main_window, width, height):
    """Centers the main window on the screen."""
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    x_position = (screen_width - width) / 2
    y_position = (screen_height - height) / 2
    main_window.geometry('%dx%d+%d+%d' % (width, height, x_position, y_position))


def center_child_window(parent_window, child_window, parent_width, parent_height, child_width,
                        child_height):
    """Centers a child window relative to its parent window."""
    parent_x_position = parent_window.winfo_x()
    parent_y_position = parent_window.winfo_y()
    x_position = (parent_width - child_width) / 2 + parent_x_position
    y_position = (parent_height - child_height) / 2 + parent_y_position
    child_window.geometry('%dx%d+%d+%d' % (child_width, child_height, x_position, y_position))
