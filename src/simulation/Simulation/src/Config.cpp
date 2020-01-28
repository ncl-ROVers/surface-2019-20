#include "Config.h"

#include "json/json11.hpp"

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
	if (!(obj = &root["mass"])->is_null() && obj->is_number())
	{
		m_rovMass = obj->number_value();
	}

	if (!(obj = &root["pos"])->is_null() && obj->is_array())
	{
		const Json::array& coords = obj->array_items();
		
		m_rovPosition = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if (!(obj = &root["rot"])->is_null() && obj->is_array())
	{
		const Json::array& coords = obj->array_items();

		m_rovRotation = { (float)coords[0].number_value(), (float)coords[1].number_value(), (float)coords[2].number_value() };
	}

	if (!(obj = &root["thrusters"])->is_null() && obj->is_object())
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

	if (!(obj = &root["scene"])->is_null() && obj->is_string())
	{
		m_useGridScene = obj->string_value() == "grid";
	}
}