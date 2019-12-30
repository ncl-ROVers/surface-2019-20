#pragma once

#include "Entity.h"

class EntityObject : public Entity
{
private:

public:
	EntityObject() {}

	void update(double delta) override;
	void render() override;
};