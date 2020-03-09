import subprocess
import os
import inspect

file_location = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
tj_root = os.path.join(file_location, "../Dependencies/TurboJPEG")
tj_build = os.path.join(tj_root, "build")

tj_lib_path = os.path.join(tj_root, "install/lib")

found_libs = False

if os.path.exists(tj_lib_path):
	for file in os.listdir(tj_lib_path):
		if file.startswith("turbojpeg."):
			found_libs = True
			break

if not found_libs:
	if not os.path.exists(tj_build) or not os.path.isdir(tj_build):
		os.mkdir(tj_build)

	os.chdir(str(tj_build))

	p = subprocess.Popen(["cmake", "-DCMAKE_INSTALL_PREFIX:PATH=../install", ".."], cwd=str(tj_build))
	p.wait()

	p = subprocess.Popen(["cmake", "--build", ".", "--config", "release", "--target", "install"], cwd=str(tj_build))
	p.wait()