#include "Config.h"

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
	long int startIndex = 0;
	long int endIndex = 0;

	for (; endIndex < dataLength;)
	{
		while ((data[endIndex] != '\r' && data[endIndex] != '\n') && endIndex < dataLength) endIndex++;

		//Process line
		const char* line = &data[startIndex];

		if (!strncmp(line, "MASS", 4))
		{
			double mass;

			sscanf_s(line, "MASS %lf", &mass);

			m_rovMass = mass;
		}
		else if (!strncmp(line, "POS", 3))
		{
			glm::vec3 position;

			sscanf_s(line, "POS %f %f %f", &position.x, &position.y, &position.z);

			m_rovPosition = position;
		}
		else if (!strncmp(line, "ROT", 3))
		{
			glm::vec3 rotation;

			sscanf_s(line, "ROT %f %f %f", &rotation.x, &rotation.y, &rotation.z);

			m_rovRotation = rotation;
		}
		else if (!strncmp(line, "T_", 2))
		{
			const char* indices = line + 2;
			int index = 0;

			index += (indices[0] == 'V') ? 4 : 0;
			index += (indices[1] == 'A') ? 2 : 0;
			index += (indices[2] == 'S') ? 1 : 0;
			
			float power = 0.0f;
			sscanf_s(line + 6, "%f", &power);

			m_thrusterPower[index] = power;
		}
		else if (!strncmp(line, "SCENE", 5))
		{
			m_useGridScene = !strncmp(line + 6, "GRID", 4);
		}

		startIndex = ++endIndex;
	}
}