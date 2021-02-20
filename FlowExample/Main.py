import argparse
import pathlib
import os
import tkinter as tk
import pandas as pd
def display_splash():


    root = tk.Tk()
    # show no frame
    root.overrideredirect(True)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' % (width * 0.8, height * 0.8, width * 0.1, height * 0.1))

    # take a .jpg picture you like, add text with a program like PhotoFiltre
    image_file =pathlib.Path.joinpath(pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(),'resources'), 'splash.gif')
    # assert os.path.exists(image_file)
    # use Tkinter's PhotoImage for .gif files
    image = tk.PhotoImage(file=image_file)
    canvas = tk.Canvas(root, height=height * 0.8, width=width * 0.8, bg="white")
    canvas.create_image(width * 0.8 / 2, height * 0.8 / 2, image=image)
    canvas.pack()

    # show the splash screen for 5000 milliseconds then destroy
    root.after(2000, root.destroy)
    root.mainloop()


def validate_input_files(input_Dir,logs_Dir):
    try:
        if(not pathlib.Path.exists(pathlib.Path(input_Dir))):
            print(f"there is no input file {input_Dir}")
            return False
        out_path=pathlib.Path(logs_Dir)
        if (not out_path.exists()):
            print(f"there is creating log dir {logs_Dir}")
            out_path.mkdir(parents=True,exist_ok=True)

        return True
    except Exception as e:
        print(f"Encoutered an error {e}")
        return False
def ProcessTestData(input_Dir,logs_Dir):
    data_full=pd.read_csv(input_Dir)
    k=0
if __name__ == "__main__":
    parser =argparse.ArgumentParser("This is the argument parser for this example -we use https://www.kaggle.com/shivamb/netflix-shows data set")
    parser.add_argument("Input_Dir",type=str,help="the folder from which to read the input")
    parser.add_argument("Logs_Dir",type=str,help="the folder from which to write output")
    args=parser.parse_args()
    if (validate_input_files(args.Input_Dir,args.Logs_Dir)):
        #display_splash()
        ProcessTestData(args.Input_Dir,args.Logs_Dir)