#pragma once

#include "Entity.h"
#include "graphics/Mesh.h"
#include "graphics/Shader.h"
#include "graphics/Texture.h"

struct PhysicsData
{
	float mass = 1.0f;

	glm::vec3 linearForce = glm::vec3(0.0f);
	glm::vec3 linearVelocity = glm::vec3(0.0f);
};

class EntityObject : public Entity
{
private:
	Mesh m_mesh;
	Shader m_shader;
	Texture m_texture;

	PhysicsData m_physicsData;
public:
	EntityObject(const std::string& modelPath, const std::pair<std::string, std::string>& shaderPaths, const std::string& albedo);
	~EntityObject();

	void update(double delta) override;
	void render(const World& world) override;

	inline void addForce(const glm::vec3& force) { m_physicsData.linearForce += force; }
	inline void addAcceleration(const glm::vec3& acceleration) { addForce(acceleration * m_physicsData.mass); }
	inline glm::vec3 getLinearForce() const { return m_physicsData.linearForce; }

	inline PhysicsData& getPhysicsData() { return m_physicsData; }
	inline const PhysicsData& getPhysicsData() const { return m_physicsData; }

	inline glm::vec3 getLinearVelocity() const {}
};