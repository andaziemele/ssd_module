# source: https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_quick_guide.htm

rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                           'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')


# function to translate plain text
def rot13(text):
    return text.translate(rot13trans)


# function to take an input text file and output encrypted file.
def encrypt_file(input_file, output_file):
    try:
        # read input file
        with open(input_file, 'r') as f:
            text = f.read()

        # encrypt the content using ROT13
        encrypted_text = rot13(text)

        # write to output file
        with open(output_file, 'w') as f:
            f.write(encrypted_text)

        print(f"File encrypted successfully. Output saved to {output_file}")
    except FileNotFoundError:
        print("Input file not found!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    # quick CLI logic
    input_file = input("Enter input file path: ")
    output_file = input("Enter output file path: ")
    encrypt_file(input_file, output_file)


if __name__ == "__main__":
    main()
