#version 430 core

layout(location = 0) in vec2 inTexCoords;
layout(location = 1) in vec3 inWorldPos;
layout(location = 2) in vec3 inNormal;

layout(location = 0) out vec4 outColor;

uniform sampler2D albedo;

void main() {
	vec3 lightPos = vec3(0.0, 2.5, 0.0);
	
	vec3 toLight = lightPos - inWorldPos;
	float lightDistance = length(toLight);
	toLight = normalize(toLight);

	float lighting = max(dot(inNormal, toLight), 0) * (1.0 / (lightDistance * lightDistance));
	//outColor = vec4(texture(albedo, inTexCoords).xyz * lighting, 1.0);
	outColor = texture(albedo, inTexCoords);
}