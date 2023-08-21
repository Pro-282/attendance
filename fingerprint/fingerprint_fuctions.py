import adafruit_fingerprint

import time
import serial

  # uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def initialize_fingerprint_sensor():
  if finger.verify_password():
    print("Fingerprint sensor initialized")
  else:
    raise ValueError("Fingerprint sensor password verification failed")

def get_fingerprint():
  """Get a finger print image, template it, and see if it matches!"""
  print("Waiting for image...")
  while finger.get_image() != adafruit_fingerprint.OK:
      pass
  print("Templating...")
  if finger.image_2_tz(1) != adafruit_fingerprint.OK:
      return False
  print("Searching...")
  if finger.finger_search() != adafruit_fingerprint.OK:
      return False
  return True

# pylint: disable=too-many-statements
def enroll_finger(location):
  """Take a 2 finger images and template it, then store in 'location'"""
  for fingerimg in range(1, 3):
    if fingerimg == 1:
        print("Place finger on sensor...", end="")
    else:
        print("Place same finger again...", end="")

    while True:
      i = finger.get_image()
      if i == adafruit_fingerprint.OK:
          print("Image taken")
          break
      if i == adafruit_fingerprint.NOFINGER:
          print(".", end="")
      elif i == adafruit_fingerprint.IMAGEFAIL:
          print("Imaging error")
          return False
      else:
          print("Other error")
          return False

      print("Templating...", end="")
      i = finger.image_2_tz(fingerimg)
      if i == adafruit_fingerprint.OK:
        print("Templated")
      else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

      if fingerimg == 1:
        print("Remove finger")
        time.sleep(1)
        while i != adafruit_fingerprint.NOFINGER:
            i = finger.get_image()

  print("Creating model...", end="")
  i = finger.create_model()
  if i == adafruit_fingerprint.OK:
    print("Created")
  else:
    if i == adafruit_fingerprint.ENROLLMISMATCH:
        print("Prints did not match")
    else:
        print("Other error")
    return False

  print("Storing model #%d..." % location, end="")
  i = finger.store_model(location)
  if i == adafruit_fingerprint.OK:
    print("Stored")
  else:
    if i == adafruit_fingerprint.BADLOCATION:
        print("Bad storage location")
    elif i == adafruit_fingerprint.FLASHERR:
        print("Flash storage error")
    else:
        print("Other error")
    return False

  return True

def get_num(max_number):
  """Use input() to get a valid number from 0 to the maximum size
  of the library. Retry till success!"""
  i = -1
  while (i > max_number - 1) or (i < 0):
    try:
      i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
    except ValueError:
      pass
  return i


while (0):
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates: ", finger.templates)
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Number of templates found: ", finger.template_count)
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to get system parameters")
    print("Size of template library: ", finger.library_size)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("s) save fingerprint image")
    print("r) reset library")
    print("q) quit")
    print("----------------")
    c = input("> ")

    if c == "e":
        enroll_finger(get_num(finger.library_size))
    if c == "f":
        if get_fingerprint():
            print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        else:
            print("Finger not found")
    if c == "d":
        if finger.delete_model(get_num(finger.library_size)) == adafruit_fingerprint.OK:
            print("Deleted!")
        else:
            print("Failed to delete")
    # if c == "s":
    #     if save_fingerprint_image("fingerprint.png"):
    #         print("Fingerprint image saved")
    #     else:
    #         print("Failed to save fingerprint image")
    if c == "r":
        if finger.empty_library() == adafruit_fingerprint.OK:
            print("Library empty!")
        else:
            print("Failed to empty library")
    if c == "q":
        print("Exiting fingerprint example program")
        raise SystemExit