workspace "ROVSimulation"
	configurations { "Debug", "Release" }
	platforms { "Win32", "x64" }
	
	filter "platforms:Win32"
      architecture "x86"

   filter "platforms:x64"
      architecture "x86_64"

outputdir = "%{cfg.buildcfg}/%{cfg.system}/%{cfg.architecture}"

project "GLAD"
	location "Dependencies/GLAD/"
	kind "StaticLib"
	language "C"
	
	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin/intermediate/" .. outputdir .. "/%{prj.name}")
	
	files { "Dependencies/%{prj.name}/src/glad.c" }
	includedirs { "Dependencies/%{prj.name}/include/" }
	
	staticruntime "On"
	systemversion "latest"
	
	filter "configurations:Debug"
		runtime "Debug"
		symbols "on"

	filter "configurations:Release"
		runtime "Release"
		optimize "on"

project "GLFW"
	location "Dependencies/GLFW/"
	kind "StaticLib"
	language "C"

	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin/intermediate/" .. outputdir .. "/%{prj.name}")

	projsrc = "Dependencies/%{prj.name}/"

	files
	{
		projsrc .. "include/GLFW/glfw3.h",
		projsrc .. "include/GLFW/glfw3native.h",
		projsrc .. "src/glfw_config.h",
		projsrc .. "src/context.c",
		projsrc .. "src/init.c",
		projsrc .. "src/input.c",
		projsrc .. "src/monitor.c",
		projsrc .. "src/vulkan.c",
		projsrc .. "src/window.c"
	}

	filter "system:linux"
		pic "On"

		systemversion "latest"
		staticruntime "On"

		files
		{
			projsrc .. "src/x11_init.c",
			projsrc .. "src/x11_monitor.c",
			projsrc .. "src/x11_window.c",
			projsrc .. "src/xkb_unicode.c",
			projsrc .. "src/posix_time.c",
			projsrc .. "src/posix_thread.c",
			projsrc .. "src/glx_context.c",
			projsrc .. "src/egl_context.c",
			projsrc .. "src/osmesa_context.c",
			projsrc .. "src/linux_joystick.c"
		}

		defines { "_GLFW_X11" }

	filter "system:windows"
		systemversion "latest"
		staticruntime "On"

		files
		{
			projsrc .. "src/win32_init.c",
			projsrc .. "src/win32_joystick.c",
			projsrc .. "src/win32_monitor.c",
			projsrc .. "src/win32_time.c",
			projsrc .. "src/win32_thread.c",
			projsrc .. "src/win32_window.c",
			projsrc .. "src/wgl_context.c",
			projsrc .. "src/egl_context.c",
			projsrc .. "src/osmesa_context.c"
		}

		defines {  "_GLFW_WIN32", "_CRT_SECURE_NO_WARNINGS" }

	filter "configurations:Debug"
		runtime "Debug"
		symbols "on"

	filter "configurations:Release"
		runtime "Release"
		optimize "on"

project "Simulation"
	location "Simulation"
	kind "ConsoleApp"
	language "C++"
	cppdialect "C++17"
	
	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin/intermediate/" .. outputdir .. "/%{prj.name}")
	
	staticruntime "On"
	systemversion "latest"
	
	files { "%{prj.name}/src/**.h", "%{prj.name}/src/**.cpp" }

	includedirs {
		"%{prj.name}/src/",
		"Dependencies/GLFW/include/",
		"Dependencies/GLAD/include",
		"Dependencies/glm/glm/"
	}
	
	links { "GLFW", "GLAD", "opengl32.lib" }
	
	filter "configurations:Debug"
		defines { "BUILD_DEBUG" }
		symbols "On"

   filter "configurations:Release"
		defines { }
		optimize "On"