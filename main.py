import main_window as mw
import login_window as lw

if __name__ == "__main__":
    
    # login window
    Login_process = lw.Login_Window()
    result = Login_process.run()

    # login completed
    # main
    if result:
        main_win = mw.Main(result[0],result[1])
        result = main_win.run()