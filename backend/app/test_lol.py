import subprocess

image_path = r"M:\Work\GIT\noteshift\test123.png"
output_folder = "output_xml"

result = subprocess.run([
    r"M:\Programs\Audiveris\Audiveris.exe",
    "-batch", "-export",
    "-output", output_folder,
    image_path
], capture_output=True, text=True)

print("Return code:", result.returncode)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
