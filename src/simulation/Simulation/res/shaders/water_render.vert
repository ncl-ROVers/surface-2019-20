#version 430

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;

layout(location = 0) out vec2 outTexCorods;
layout(location = 1) out vec3 outNormal;
layout(location = 2) out float outHeight;

uniform mat4 transform;
uniform double time;

float sine_height(vec2 pos, float angle, float wavelength, float kAmpOverLen, float speed, double time) {
	float freq = 2.0 / wavelength;
	float phaseSpeed = speed * freq;
	vec2 direction = vec2(cos(angle), sin(angle));
	
	return (kAmpOverLen * wavelength) * sin(dot(direction, pos) * freq + float(time) * phaseSpeed);
}

vec2 sine_height_derv(vec2 pos, float angle, float wavelength, float kAmpOverLen, float speed, double time) {
	float freq = 2.0 / wavelength;
	float phaseSpeed = speed * freq;
	vec2 direction = vec2(cos(angle), sin(angle));
	
	float hCos = (kAmpOverLen * wavelength) * cos(dot(direction, pos) * freq + float(time) * phaseSpeed);
	return direction * (freq * hCos);
}

void main() {
	outTexCorods = texCoords;
	
	vec4 wave_info[15];
wave_info[0] = vec4(1.9938976857396, 3.820761180555417, 0.013342024123185052, 2.496143727852127);
wave_info[1] = vec4(4.606207583708874, 1.346114685351201, 0.007394243154531832, 0.22976168063606417);
wave_info[2] = vec4(2.251463692193873, 3.887339913687039, 0.045190005963234914, 0.9560939611174311);
wave_info[3] = vec4(5.829563684222491, 3.300823143105748, 0.004958314701450835, 0.5405418610536304);
wave_info[4] = vec4(3.672871994271655, 1.7213682441266582, 0.022800124229581702, 0.8285291398224299);
wave_info[5] = vec4(4.981653356198379, 3.3481891602381455, 0.06426667265090584, 4.06878245689934);
wave_info[6] = vec4(3.219930731973856, 1.3503986602117126, 0.05721683606394984, 4.816290321467228);
wave_info[7] = vec4(3.6570021184710915, 2.1446589265664837, 0.0207538235726001, 0.6396514736219341);
wave_info[8] = vec4(5.450407758966196, 1.2285777894757324, 0.009822788805511662, 0.6718367589640216);
wave_info[9] = vec4(0.6409372517055179, 2.2509734642140433, 0.051936306608145355, 6.8597535523353015);
wave_info[10] = vec4(6.2769359433687875, 1.6762648254714478, 0.014444651790728935, 1.896624566191736);
wave_info[11] = vec4(2.3754464061814837, 2.138386513752543, 0.05524518157850767, 6.340845105544454);
wave_info[12] = vec4(6.179689009296739, 2.7910095173465, 0.04374658616396728, 4.699860638991206);
wave_info[13] = vec4(5.735776108731809, 3.9817173086635305, 0.010922678585536779, 5.842394464376261);
wave_info[14] = vec4(0.03001704119353672, 3.123508499377433, 0.059208695898274426, 5.48510108350384);

	
	float offset = 0.0;
	vec2 dH = vec2(0.0);

	for(int i = 0; i < 15; ++i) {
		offset += sine_height(position.xz, wave_info[i].x, wave_info[i].y, wave_info[i].z, wave_info[i].w, time);
		dH += sine_height_derv(position.xz, wave_info[i].x, wave_info[i].y, wave_info[i].z, wave_info[i].w, time);
	}
	
	outNormal = normalize(vec3(-dH.x, 1, -dH.y));
	outHeight = 1.5 * (0.5 * offset + 0.5);
	
	gl_Position = transform * vec4(position + vec3(0, offset, 0), 1.0);
}