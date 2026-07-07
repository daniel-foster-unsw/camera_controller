import os



class ConsoleMenu:

    def __init__(self, application):

        self.application = application
    #Header class
    def display_header(self):

        status = self.application.get_system_header()

        print("=" * 60)
        print("         CORE SCANNER CAMERA CONTROLLER")
        print("=" * 60)

        print(f"Camera State : {status['camera_state']}")
        print(f"Camera Driver: {status['camera_driver']}")
        print(f"Camera ID    : {status['camera_id']}")

        print()

        print(f"Storage      : {status['storage']}")
        print(f"Images Taken : {status['images_taken']}")

        print()

        print(f"Logger       : {status['log_level']}")
        print(f"Log File     : {status['log_file']}")

        print("=" * 60)

    #Menu Display
    def display(self):

        print("\n==============================================")
        print("      CORE SCANNER CAMERA CONTROLLER")
        print("==============================================")

        print("\n1. Capture Test Image")
        print("2. Camera Information")
        print("3. Camera Status")
        print("4. Storage Information")
        print("5. Configuration")
        print("6. Camera Self Test")
        print("7. System Status")
        print("8. View Log File")
        print("9. Clear Screen")
        print("0. Exit")

        print("==============================================")




    #Read User Input
    def get_selection(self):

        return input("\nSelect Option > ").strip()
        

        #Run Menu
    def run(self):

        while True:

            self.display()

            choice = self.get_selection()

            if choice == "1":
                self.application.capture_test_image()

            elif choice == "2":
                info = self.application.show_camera_information()
                print(info)

            elif choice == "3":
                info = self.application.show_camera_status()
                print(info)

            elif choice == "4":
                info = self.application.show_storage_information()
                print(info)

            elif choice == "5":
                info = self.application.show_configuration()
                print(info)

            elif choice == "6":
                info = self.application.run_camera_self_test()
                print(info)

            elif choice == "7":
                #info = self.application.show_system_status()
                #print(info)
                status = self.application.get_system_header()

                print(f"Camera State : {status['camera_state']}")
                print(f"Camera Driver: {status['camera_driver']}")
                print(f"Camera ID    : {status['camera_id']}")

                print()

                print(f"Storage      : {status['storage']}")
                print(f"Images Taken : {status['images_taken']}")

                print()

                print(f"Logger       : {status['log_level']}")
                print(f"Log File     : {status['log_file']}")

                print("=" * 60)







            elif choice == "8":
                info = self.application.show_log_location()
                print(info)

                

            elif choice == "9":
                self.clear_screen()

            elif choice == "0":
                break

            else:
                print("\nInvalid selection.")


        #Clear Screen

    def clear_screen(self):

        os.system("cls" if os.name == "nt" else "clear")


       


        
        