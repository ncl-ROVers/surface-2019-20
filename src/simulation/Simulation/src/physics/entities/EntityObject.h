#pragma once

#include "Entity.h"
#include "graphics/Mesh.h"
#include "graphics/Shader.h"
#include "graphics/Texture.h"

#include "physics/RigidBody.h"

class EntityObject : public Entity
{
private:
	Mesh m_mesh;
	Shader m_shader;
	Texture m_texture;

	RigidBodyData m_rigidBody;
public:
	EntityObject(const std::string& modelPath, const std::pair<std::string, std::string>& shaderPaths, const std::string& albedo);
	~EntityObject();

	void update(double delta) override;
	void render(const World& world) override;

	inline void setLinearVelocity(const glm::vec3& velocity) { m_rigidBody.linearMomentum = velocity * (float)m_rigidBody.mass; }
	inline void addLinearVelocity(const glm::vec3& velocity) { m_rigidBody.linearMomentum += velocity * (float)m_rigidBody.mass; }

	inline void addForce(const glm::vec3& force) { m_rigidBody.totalForce += force; }
	inline void addForce(const glm::vec3& pos, const glm::vec3& force) { m_rigidBody.totalTorque += glm::cross(pos, force); }
	inline void addAcceleration(const glm::vec3& acceleration) { addForce(acceleration * (float)m_rigidBody.mass); }

	inline glm::vec3 getLinearForce() const { return m_rigidBody.totalForce; }

	inline RigidBodyData& getRigidBodyData() { return m_rigidBody; }
	inline const RigidBodyData& getRigidBodyData() const { return m_rigidBody; }
};