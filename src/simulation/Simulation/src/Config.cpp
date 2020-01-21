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

		if (line[0] == 't')
		{
			int thrusterIndex = 0;
			float power = 0.0f;

			sscanf_s(line, "t%d %f", &thrusterIndex, &power);

			if (thrusterIndex > 0 || thrusterIndex < THRUSTER_COUNT)
			{
				m_thrusterPower[thrusterIndex] = power;
			}
		}
		else if (line[0] == 'm')
		{
			double mass;

			sscanf_s(line, "m %lf", &mass);

			m_rovMass = mass;
		}
		else if (line[0] == 'p')
		{
			glm::vec3 position;

			sscanf_s(line, "p %f %f %f", &position.x, &position.y, &position.z);

			m_rovPosition = position;
		}
		else if (line[0] == 'r')
		{
			glm::vec3 rotation;

			sscanf_s(line, "r %f %f %f", &rotation.x, &rotation.y, &rotation.z);

			m_rovRotation = rotation;
		}

		startIndex = ++endIndex;
	}
}