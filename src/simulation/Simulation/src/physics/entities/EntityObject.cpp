#include "EntityObject.h"

#include "Scene.h"

inline std::string toCacheName(std::string path)
{
	//Get the name of the file pointed to by the provided path
	std::string saveName = std::filesystem::path(path).filename().generic_string();

	//Remove all periods from filename
	size_t dotIndex = 0;
	while ((dotIndex = saveName.find_first_of('.')) != std::string::npos)
	{
		saveName.erase(dotIndex);
	}

	return saveName;
}

EntityObject::EntityObject(const MaterialData& materialData) :
	m_materialData(materialData)
{
	LaunchCache* cache = Scene::singleton()->getCache();

	std::string saveName = toCacheName(materialData.model);
	if (cache->isMeshOutdated(saveName, materialData.model))
	{
		LOG_VERBOSE("Loading model: ", materialData.model);
		m_mesh.load(materialData.model);
		cache->saveMeshData(saveName, m_mesh);
	}
	else
	{
		LOG_VERBOSE("Loading model from cache: ", materialData.model);
		cache->loadMeshData(saveName, m_mesh);
	}

	m_shader.init();
	m_shader.addShaderFromPath(GL_VERTEX_SHADER, materialData.vertexShader);
	m_shader.addShaderFromPath(GL_FRAGMENT_SHADER, materialData.fragmentShader);
	m_shader.compile();

	m_texture.create(materialData.albedo);
}

EntityObject::~EntityObject()
{
	m_mesh.destroy();
	m_shader.destroy();
	m_texture.destroy();
}

void EntityObject::render(RenderingEngine& renderer)
{
	const World& world = renderer.getWorld();

	glm::mat4 model = m_transform.matrix();
	glm::mat4 view = world.camera.getViewMatrix();
	glm::mat4 proj = world.camera.getProjectionMatrix();

	glm::mat4 mvpMatrix = proj * view * model;

	m_shader.bind();
	m_shader.setUniform("albedo", 0);
	m_shader.setUniform("transform", mvpMatrix);
	m_shader.setUniform("model", model);

	m_shader.setUniform("sunDirection", world.sunDirection);
	m_shader.setUniform("ambientLighting", world.ambientLight);

	m_texture.bind(0);

	m_mesh.draw();
}