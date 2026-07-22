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
        """
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
        """

        
        print("\n==============================================")
        print("      CORE SCANNER CAMERA CONTROLLER")
        print("==============================================")

        print("\n")
        print("\nCamera")
        print("----------------------------------------------")

        print("\n1. Capture Image")
        print("2. Camera Information")
        print("3. Camera Status")
        print("4. Camera Self Test")

        print("\n")
        print("\n Storage")
        print("----------------------------------------------")
        print("\n5. Storage Information")
        print("6. List Scans")
        print("7. Delete Image")
        print("8. Delete Scan")

        print("\n")
        print("\n System")
        print("----------------------------------------------")
        print("\n9. Configuration")
        print("10. System Status")
        print("11. View Log File")

        print("\n")
        print("----------------------------------------------")
        print("12. Clear Screen")
        print("0. Exit")

        print("==============================================")
        



    #Read User Input
    def get_selection(self):

        return input("\nSelect Option > ").strip()
        

        #Run Menu
    def run(self):

        while True:

            self.clear()
            
            self.display_header()
            self.display()

            choice = self.get_selection()

            if choice == "1":#capture image
                info = self.application.capture_image()
                print(info)
                self.pause()

            elif choice == "2":# Camera information
                info = self.application.get_camera_information()
                print(info)
                self.pause()

            elif choice == "3":#Camera Status
                info = self.application.get_camera_status()
                print(info)
                self.pause()

            elif choice == "4":#Camera Self Test
                #info = self.application.show_storage_information()
                info = self.application.run_camera_self_test()
                print(info)
                self.pause()

            elif choice == "5":#storage information
                info = self.application.get_storage_information()
                #info = self.application.show_configuration()
                print(info)
                self.pause()

            elif choice == "6":#list scans
                self.list_scans()
                self.pause()

            elif choice == "7":#delete image
                self.delete_image()
                self.pause()
         
            elif choice == "8":#delete scan
                self.delete_scan()
                self.pause()

            elif choice == "9":#Display Configuration
                info = self.application.get_configuration()
                print(info)
                self.pause()

            elif choice == "10":#Disply system status
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

                self.pause()
                
            elif choice == "11":#View log location
                info = self.application.get_log_location()
                print(info)
                self.pause()

            elif choice == "12":#clear screen
                self.clear()
                self.pause()

            elif choice == "0":#exit
                break

            else:#Invalid selection
                print("\nInvalid selection.")


        #Clear Screen

    def clear(self):

        os.system("cls" if os.name == "nt" else "clear")


    def list_scans(self):

        scans = self.application.list_images()

        print()

        if len(scans) == 0:
            print("No scans found.\n")
            return

        for scan in scans:

            print(scan["scan"])

            for image in scan["images"]:

                print(
                    f"    {image['filename']} "
                    f"({image['filesize']} bytes)"
                )

            print()

    def delete_image(self):

        filename = input("\nFilename: ")

        if self.application.delete_image(filename):

            print("\nImage deleted.\n")

        else:

            print("\nImage not found.\n")
        
    def delete_scan(self):

        scan = input("\nScan: ")

        confirm = input(f"Delete '{scan}'? (y/n): ")

        if confirm.lower() != "y":

            return

        if self.application.delete_scan(scan):

            print("\nScan deleted.\n")

        else:

            print("\nScan not found.\n")


    def pause(self):

        input("\nPress Enter to continue...")

