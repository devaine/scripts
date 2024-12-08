# Made by Devaine
# mostly because bash was pissing me off when it comes to recursion
# also because i am lazy and i wanted to automate things

import time
import os


class GPG():
    def export(id_num):
        print("\n\nHere's your exported key for ID: " + id_num)
        os.system("gpg --armor --export " + id_num)

    def view():
        id_output = os.popen("gpg --list-keys --with-colons | \
                          awk -F: '/^pub:/ { print $5 }'").read()
        id_split = id_output.split("\n")

        info_output = os.popen("gpg --list-keys --with-colons | \
                                 awk -F: '/^uid:/ { print $10 }'").read()
        info_split = info_output.split("\n")

        print("\n\n----------------------")
        for i in range(len(info_split) - 1):
            print("ID #" + str(i) + ": " + id_split[i] +
                  "\nInfo: " + info_split[i])

        print("\n")

        def prompt():
            question = input("ID # you want to export: ")

            while question == "":
                question = input("ID # you want to export: ")

            try:
                response = int(question)
            except ValueError:
                print("Not a valid ID number!")
                time.sleep(1)
                prompt()

            if response >= len(info_output) - 1 or response < 0:
                print("Not a valid ID number! test")
                time.sleep(1)
                prompt()
            else:
                GPG.export(id_split[response])

        prompt()

    def view_prompt():
        prompt = input("Do you want to see the entire GPG Key? (Y/N): ")
        while prompt == "":
            prompt = input("Do you want to see the entire GPG Key? (Y/N): ")

        ans = prompt.upper()

        if "Y" in ans:
            GPG.view()

        elif "N" in ans:
            print("Exiting...")
            exit(0)
        else:
            print("Incorrect Reponse!")
            print("Retrying...")
            time.sleep(1)
            GPG.view_prompt()

    def gpg_keygen():
        os.system("gpg --full-generate-key")

    def __init__():
        GPG.gpg_keygen()
        GPG.view_prompt()


class SSH():
    def keygen():
        def fileDestination():
            default_destination = os.path.expanduser("~") + "/.ssh"
            print("------------")
            print("Default: " + default_destination)
            prompt = input("Path for Key (Press Enter for Default): ")

            if prompt == "":
                prompt = default_destination

            if os.path.exists(prompt) is True:
                os.system("ssh-keygen -f " + prompt + "/" + name + " -t ed25519")
            else:
                print("Path " + prompt + " doesn't exist, try again.")
                time.sleep(1)
                fileDestination()

        def nameConfirmation(confirm):
            while confirm == "":
                confirm = input("Are you sure this is the name you want? (Y/N): ")
            ans = confirm.upper()

            if "Y" in ans:
                fileDestination()

            elif "N" in ans:
                print("Retrying...")
                SSH.keygen()

            else:
                print("Incorrect Reponse!")
                print("Retrying...")
                time.sleep(1)
                nameConfirmation()
        # Function starts here actually.
        name = input("What is the name of your key: ")

        while name == "":
            name = input("What is the name of your key: ")

        confirm = input("Are you sure this is the name you want (" + name + ")? (Y/N): ")
        nameConfirmation(confirm)

    def gpg_prompt():
        prompt = input("Do you want to create a GPG Key? (Y/N): ")
        while prompt == "":
            prompt = input("Do you want to create a GPG Key? (Y/N): ")
        ans = prompt.upper()
        if "Y" in ans:
            print("Starting...")
            GPG.gpg_keygen()
        elif "N" in ans:
            GPG.view_prompt()

        else:
            print("Incorrect Reponse!")
            time.sleep(1)
            SSH.gpg_prompt()

    def public_key_view():
        def choose_file():
            default_destination = os.path.expanduser("~") + "/.ssh"
            print("------------")
            print("Default Path: " + default_destination)
            path = input("Enter Key Path (Press Enter for Default): ")

            if path == "":
                path = default_destination

            if os.path.exists(path) is True:
                avail_options = os.popen("ls " + path + "| grep .pub").read()
            else:
                print("Path " + path + " doesn't exist, try again.")
                time.sleep(1)
                choose_file()

            options_split = avail_options.split("\n")

            print("There are " + str(len(options_split) - 1)
                  + " public keys available to read...")

            for i in range(len(options_split) - 1):
                print("Option #" + str(i) + ": " + options_split[i][:-4])

            def prompt():
                question = input("Choose an option (by number): ")

                while question == "":
                    question = input("Choose an option (by number): ")

                try:
                    response = int(question)
                except ValueError:
                    print("Not a valid number!")
                    time.sleep(1)
                    prompt()

                if response >= len(options_split) - 1 or response < 0:
                    print("Not a valid ID number! test")
                    time.sleep(1)
                    prompt()
                else:
                    print("Here's the public key from Option #" + str(i)
                          + " (" + options_split[response] + "):")
                    os.system("cat " + path + "/" + options_split[response])

            prompt()

        prompt = input("Do you want to view your SSH public key? (Y/N): ")
        while prompt == "":
            prompt = input("Do you want to view your SSH public key? (Y/N): ")
        ans = prompt.upper()
        if "Y" in ans:
            print("Starting...")
            choose_file()

        elif "N" in ans:
            SSH.gpg_prompt()

        else:
            print("Incorrect Reponse!")
            time.sleep(1)
            SSH.public_key_view()

    def start():
        ssh_prompt = input("Do you want to create a SSH Key? (Y/N): ")
        while ssh_prompt == "":
            ssh_prompt = input("Do you want to create a SSH Key? (Y/N): ")
        ans = ssh_prompt.upper()

        if "Y" in ans:
            print("Starting...")
            SSH.keygen()

        elif "N" in ans:
            SSH.public_key_view()

        else:
            print("Incorrect Reponse!")
            time.sleep(1)
            SSH.start()


if __name__ == "__main__":
    SSH.start()
