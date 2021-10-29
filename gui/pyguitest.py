import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo


def cb():
    print("Called")


def main():
    with dpg.window(label="Example", tag="Primary Window", width=200, height=200):
        dpg.add_text("Yo")
        dpg.add_input_text(label="string", default_value="Default value")
        dpg.add_button(label="Button", callback=cb)
    # show_demo()


if __name__ == "__main__":
    dpg.create_context()

    main()

    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
