#pragma once

#include <sstream>
#include <mutex>

enum LogLevel
{
	LOG_LEVEL_VERBOSE,
	LOG_LEVEL_DEBUG,
	LOG_LEVEL_WARNING,
	LOG_LEVEL_ERROR
};

class Logger
{
private:
	std::mutex m_logMutex;

	static Logger s_instance;
private:
	Logger() {}
	~Logger() {}

	template<typename First>
	void printInternal(std::ostream& ss, First&& first)
	{
		ss << first;
	}

	template<typename First, typename ... Args>
	void printInternal(std::ostream& ss, First&& first, Args&& ... args)
	{
		ss << first;

		if (sizeof...(args))
		{
			printInternal(ss, std::forward<Args>(args)...);
		}
	}

	template<typename ... Args>
	void print(LogLevel level, Args&& ... args)
	{
		std::stringstream ss;
		printInternal(ss, std::forward<Args>(args)...);

		pushMessage(level, ss.str());
	}

	void pushMessage(LogLevel level, const std::string& str);
public:
	template<typename ... Args>
	void verbose(Args&& ... args) { print(LOG_LEVEL_VERBOSE, std::forward<Args>(args)...); }

	template<typename ... Args>
	void debug(Args&& ... args) { print(LOG_LEVEL_DEBUG, std::forward<Args>(args)...); }

	template<typename ... Args>
	void warning(Args&& ... args) { print(LOG_LEVEL_WARNING, std::forward<Args>(args)...); }

	template<typename ... Args>
	void error(Args&& ... args) { print(LOG_LEVEL_ERROR, std::forward<Args>(args)...); }

	void pause();

	static Logger* singleton();
};

#define LOG_VERBOSE(...) Logger::singleton()->verbose(__VA_ARGS__)
#define LOG_DEBUG(...) Logger::singleton()->debug(__VA_ARGS__)
#define LOG_WARN(...) Logger::singleton()->warning(__VA_ARGS__)
#define LOG_ERROR(...) Logger::singleton()->error(__VA_ARGS__)
#define LOG_PAUSE() Logger::singleton()->pause();