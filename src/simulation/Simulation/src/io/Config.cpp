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

const char* typeName(json11::Json::Type type)
{
	using namespace json11;

	switch (type)
	{
	case Json::NUL: return "NULL";
	case Json::NUMBER: return "NUMBER";
	case Json::BOOL: return "BOOL";
	case Json::STRING: return "STRING";
	case Json::ARRAY: return "ARRAY";
	case Json::OBJECT: return "OBJECT";
	}

	return "Unknown";
}

bool isFieldOfType(const json11::Json* obj, const char* name, json11::Json::Type type)
{
	if (obj->type() == json11::Json::NUL)
	{
		return false;
	}

	if (obj->type() != type)
	{
		LOG_WARN("JSON field '", name, "' should be of type '", typeName(type), "' not '", typeName(obj->type()), "'! Ignoring field.");
		return false;
	}

	return true;
}

bool isValidArray(const json11::Json* obj, const char* name, size_t requiredSize)
{
	if (!isFieldOfType(obj, name, json11::Json::ARRAY))
	{
		return false;
	}

	const json11::Json::array& asArray = obj->array_items();

	if (asArray.size() != requiredSize)
	{
		LOG_WARN("JSON array '", name, "' (size=", asArray.size(), ") is not the correct size(", requiredSize, ").");
		return false;
	}

	return true;
}

void Config::loadConfig(const std::string& path)
{
	long int size = 0;
	byte* src = readFileContent(resolvePath(path), size);

	if (!src)
	{
		LOG_ERROR("Unable to open config file.");
		return;
	}

	loadConfigFromMemory((const char*)src, size);

	delete[] src;
}

void parseROVData(const json11::Json& root, RovSetup& rov)
{
	using namespace json11;
	
	const Json* obj = nullptr;
	if (isFieldOfType(obj = &root["mass"], "mass", Json::NUMBER))
	{
		rov.mass = obj->number_value();
	}

	if (isValidArray(obj = &root["pos"], "pos", 3))
	{
		const Json::array& coords = obj->array_items();

		rov.position = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if (isValidArray(obj = &root["rot"], "rot", 3))
	{
		const Json::array& coords = obj->array_items();

		rov.rotation = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if (isFieldOfType(obj = &root["thrusters"], "thrusters", Json::OBJECT))
	{
		for (const std::pair<std::string, Json>& thruster : obj->object_items())
		{
			//Calculate thruster index based on its name
			int index = 0;
			index += (thruster.first[0] == 'v') ? 4 : 0;
			index += (thruster.first[1] == 'a') ? 2 : 0;
			index += (thruster.first[2] == 's') ? 1 : 0;

			const Json* comp = nullptr;
			if (isValidArray(comp = &thruster.second["pos"], "pos", 3))
			{
				const Json::array& coords = comp->array_items();

				rov.thrusterPositions[index] = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
			}

			if (isValidArray(comp = &thruster.second["rot"], "rot", 3))
			{
				const Json::array& coords = comp->array_items();

				rov.thrusterRotations[index] = glm::vec3((float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value());
			}

			if (isFieldOfType(comp = &thruster.second["force"], "force", Json::NUMBER))
			{
				rov.thrusterPower[index] = (float)comp->number_value();
			}
		}
	}

	if (isFieldOfType(obj = &root["cameras"], "cameras", Json::ARRAY))
	{
		for (const Json& thruster : obj->array_items())
		{
			ROVCameraSetup camSetup;

			const Json* comp = nullptr;
			if (isValidArray(comp = &thruster["pos"], "pos", 3))
			{
				const Json::array& coords = comp->array_items();

				camSetup.position = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
			}

			if (isValidArray(comp = &thruster["rot"], "rot", 3))
			{
				const Json::array& coords = comp->array_items();

				camSetup.rotation = glm::vec3((float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value());
			}

			if (isValidArray(comp = &thruster["resolution"], "resolution", 2))
			{
				const Json::array& size = comp->array_items();

				camSetup.resolution = glm::vec2((float)size[0].number_value(), (float)size[1].number_value());
			}

			if (isFieldOfType(comp = &thruster["fov"], "fov", Json::NUMBER))
			{
				camSetup.fov = (float)comp->number_value();
			}

			if (isFieldOfType(comp = &thruster["port"], "port", Json::NUMBER))
			{
				camSetup.port = (int)comp->number_value();
			}

			if (isFieldOfType(comp = &thruster["quality"], "quality", Json::NUMBER))
			{
				camSetup.quality = std::clamp((int)comp->number_value(), 1, 100);
			}

			rov.cameras.push_back(camSetup);
		}
	}

	if (isValidArray(obj = &root["center_of_mass"], "center_of_mass", 3))
	{
		const Json::array& coords = obj->array_items();

		rov.centerOfMass = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if (isFieldOfType(obj = &root["max_thruster_force"], "max_thruster_force", Json::NUMBER))
	{
		rov.maxThrsuterPower = (float)obj->number_value();
	}

	if (isFieldOfType(obj = &root["server_port"], "server_prot", Json::NUMBER))
	{
		rov.serverPort = (int)obj->number_value();
	}
}

void Config::loadConfigFromMemory(const char* data, long int dataLength)
{
	using namespace json11;

	std::string err;
	Json root = Json::parse(std::string(data, dataLength), err);

	if (!err.empty())
	{
		LOG_ERROR("Error parsing config file: ", err);
		return;
	}

	const Json* obj = nullptr;
	if (isFieldOfType(obj = &root["rov_setup"], "rov_setup", Json::OBJECT))
	{
		parseROVData(*obj, m_rov);
	}

	if (isFieldOfType(obj = &root["scene"], "scene", Json::STRING))
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
			LOG_WARN("Scene type '", obj->string_value(), "' not recognized!");
			LOG_WARN("Setting scene type to default.");
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
				LOG_WARN("Headless simulation support is not currently supported!");
				LOG_WARN("Switching to first peson camera.");
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
					const Json::array& coords = prop.second.array_items();

					m_cameraSettings.position = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
				}
				else if (prop.first == "pitch" && isFieldOfType(&prop.second, "pitch", Json::NUMBER))
				{
					m_cameraSettings.pitch = (float)prop.second.number_value();
				}
				else if (prop.first == "yaw" && isFieldOfType(&prop.second, "yaw", Json::NUMBER))
				{
					m_cameraSettings.yaw = (float)prop.second.number_value();
				}
				else if (prop.first == "fov" && isFieldOfType(&prop.second, "fov", Json::NUMBER))
				{
					m_cameraSettings.fov = (float)prop.second.number_value();
				}
				else if (prop.first == "allowMovement" && isFieldOfType(&prop.second, "allowMovement", Json::BOOL))
				{
					m_cameraSettings.allowMovement = prop.second.bool_value();
				}
				else if (prop.first == "allowLooking" && isFieldOfType(&prop.second, "allowLooking", Json::BOOL))
				{
					m_cameraSettings.allowLooking = prop.second.bool_value();
				}
			}
		}
		else
		{
			LOG_WARN("JSON field 'camera' should be either a string or an object, not '", typeName(obj->type()), "'.");
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
		else
		{
			LOG_WARN("JSON field 'cache' should be either a string or a boolean, not '", typeName(obj->type()), "'.");
		}
	}
}