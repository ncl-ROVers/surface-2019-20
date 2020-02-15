#pragma once

#include "Common.h"
#include "physics/Transform.h"
#include "graphics/World.h"

#include "graphics/RenderingEngine.h"

#include <cstdint>

class Entity
{
protected:
	Transform m_transform;
	Entity* m_parent = nullptr;
	std::vector<Entity*> m_children;
public:
	Entity() {}
	Entity(const Entity& other) = delete;
	virtual ~Entity() {}

	virtual void update(double delta) {}
	virtual void render(RenderingEngine& renderer) {}

	inline void operator=(const Entity& other) = delete;

	inline void setParent(Entity* parent)
	{
		if (m_parent)
		{
			std::vector<Entity*>::const_iterator it = std::find(m_parent->m_children.begin(), m_parent->m_children.end(), this);
			if (it != m_parent->m_children.end())
			{
				m_parent->m_children.erase(it);
			}
		}

		m_parent = nullptr;
		m_transform.parent(nullptr);

		if (parent)
		{
			parent->m_children.push_back(this);
			m_parent = parent;

			m_transform.parent(&m_parent->m_transform);
		}
	}

	inline void setTransform(const Transform& transform) { m_transform = transform; }
	inline const Transform& getTransform() const { return m_transform; }
	inline Transform& getTransform() { return m_transform; }
};