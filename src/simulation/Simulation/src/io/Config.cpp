#include "Config.h"

#include "json/json11.hpp"

CameraSettings firstPersonCamera()
{
	CameraSettings cameraSetting;
	cameraSetting.position = glm::vec3(0.0f, 1.0f, 3.0f);
	cameraSetting.pitch = -20.0f;
	cameraSetting.yaw = 0.0f;
	cameraSetting.fov = 70.0f;

	cameraSetting.allowMovement = true;
	cameraSetting.allowLooking = true;

	return cameraSetting;
}

bool isValidArray(const json11::Json* obj, const std::string& name, size_t requiredSize)
{
	if (!obj->is_array())
	{
		std::cerr << "JSON object '" << name << "' is not an array!" << std::endl;
	}

	const json11::Json::array& asArray = obj->array_items();

	if (asArray.size() != requiredSize)
	{
		std::cerr << "JSON array '" << name << "' (size=" << asArray.size() << ") is not the correct size(" << requiredSize << ").";
		return false;
	}

	return true;
}

void Config::loadConfig(const std::string& path)
{
	long int size = 0;
	byte* src = readFileContent(std::filesystem::absolute(path).u8string(), size);

	if (!src)
	{
		std::cerr << "Unable to open config file.\n";
		return;
	}

	loadConfigFromMemory((const char*)src, size);

	delete[] src;
}

void Config::loadConfigFromMemory(const char* data, long int dataLength)
{
	using namespace json11;

	std::string err;
	Json root = Json::parse(std::string(data, dataLength), err);

	if (!err.empty())
	{
		std::cerr << "Error loading config file: " << err << std::endl;
	}

	const Json* obj = nullptr;
	if ((obj = &root["mass"])->is_number())
	{
		m_rovMass = obj->number_value();
	}

	if ((obj = &root["pos"])->is_array() && isValidArray(obj, "pos", 3))
	{
		const Json::array& coords = obj->array_items();
		
		m_rovPosition = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if ((obj = &root["rot"])->is_array() && isValidArray(obj, "rot", 3))
	{
		const Json::array& coords = obj->array_items();

		m_rovRotation = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if ((obj = &root["thrusters"])->is_object())
	{
		for (const std::pair<std::string, Json>& thruster : obj->object_items())
		{
			int index = 0;
			index += (thruster.first[0] == 'v') ? 4 : 0;
			index += (thruster.first[1] == 'a') ? 2 : 0;
			index += (thruster.first[2] == 's') ? 1 : 0;

			m_thrusterPower[index] = thruster.second.is_number() ? (float)thruster.second.number_value() : 0.0f;
		}
	}

	if ((obj = &root["scene"])->is_string())
	{
		if (obj->string_value() == "grid")
		{
			m_sceneType = SCENE_TYPE_GRID;
		}
		else if (obj->string_value() == "pool")
		{
			m_sceneType = SCENE_TYPE_POOL;
		}
		else
		{
			std::cerr << "Scene type '" << obj->string_value() << "' not recognized!" << std::endl;
			std::cerr << "Setting scene type to default." << std::endl;
		}
	}

	if (!(obj = &root["camera"])->is_null())
	{
		if (obj->is_string())
		{
			if (obj->string_value() == "firstperson")
			{
				m_cameraSettings = firstPersonCamera();
			}
			else if (obj->string_value() == "headless")
			{
				std::cerr << "Headless simulation support is not currently supported!" << std::endl;
				std::cerr << "Switching to first peson camera." << std::endl;
				m_cameraSettings = firstPersonCamera();
			}
		}
		else if (obj->is_object())
		{
			m_cameraSettings = firstPersonCamera();

			for (const std::pair<std::string, Json>& prop : obj->object_items())
			{
				if (prop.first == "pos" && isValidArray(&prop.second, "pos", 3))
				{
					const Json::array& coords = obj->array_items();

					m_cameraSettings.position = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
				}
				else if (prop.first == "pitch" && prop.second.is_number())
				{
					m_cameraSettings.pitch = (float)prop.second.number_value();
				}
				else if (prop.first == "yaw" && prop.second.is_number())
				{
					m_cameraSettings.yaw = (float)prop.second.number_value();
				}
				else if (prop.first == "fov" && prop.second.is_number())
				{
					m_cameraSettings.fov = (float)prop.second.number_value();
				}
				else if (prop.first == "allowMovement" && prop.second.is_bool())
				{
					m_cameraSettings.allowMovement = prop.second.bool_value();
				}
				else if (prop.first == "allowLooking" && prop.second.is_bool())
				{
					m_cameraSettings.allowLooking = prop.second.bool_value();
				}
			}
		}
	}
	else
	{
		m_cameraSettings = firstPersonCamera();
	}

	if (!(obj = &root["cache"])->is_null())
	{
		if (obj->is_bool())
		{
			m_cacheEnabled = obj->bool_value();
		}
		else if (obj->is_string())
		{
			m_cacheEnabled = true;
			m_cacheDir = obj->string_value();
		}
	}
}