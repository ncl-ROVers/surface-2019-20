#pragma once

#include "Common.h"
#include "physics/Transform.h"
#include "graphics/World.h"

#include <cstdint>

class Entity
{
protected:
	uint32_t m_entityID = -1;

	Transform m_transform;
public:
	Entity() {}
	Entity(const Entity& other) = delete;
	virtual ~Entity() {}

	virtual void update(double delta) = 0;
	virtual void render(const World& world) = 0;

	inline void operator=(const Entity& other) = delete;

	inline const Transform& getTransform() const { return m_transform; }
	inline Transform& getTransform() { return m_transform; }
	inline void setTransform(const Transform& transform) { m_transform = transform; }
};