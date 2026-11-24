/**
 * @file robot_identity.h
 * @brief Robot identity fields aligned with cloud data model
 * @author HTW_DEV
 * @date 2026-11-24
 * @version 2026-11-24_v0.1
 *
 * Copyright (c) 2026 Hantewin. All rights reserved.
 *
 * modify history:
 * ------------------------------------------------------------
 * | date       | author  | description                        |
 * |------------|---------|------------------------------------|
 * | 2026-11-24 | HTW_DEV | initial placeholder                |
 * ------------------------------------------------------------
 */

#ifndef HTWCLOUD_ROBOT_IDENTITY_H
#define HTWCLOUD_ROBOT_IDENTITY_H

#include <string>

namespace Hantewin {
namespace HtwCloud {

/**
 * @brief Robot identity subset shared with Python models
 * @date 2026-11-24
 * @author HTW_DEV
 */
typedef struct {
    std::string robot_id;          // robot unique id
    std::string product_id;        // product model id
    std::string hardware_version;  // hardware revision
} ROBOTIDENTITY_T;

} // namespace HtwCloud
} // namespace Hantewin

#endif // HTWCLOUD_ROBOT_IDENTITY_H
