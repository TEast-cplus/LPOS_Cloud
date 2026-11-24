/**
 * @file error_code.cpp
 * @brief HTW Cloud error code string helpers
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

#include "htw_cloud/error_code.h"

namespace Hantewin {
namespace HtwCloud {

const char* errorCodeToString(HTW_CLOUD_ERROR_E error_code)
{
    if (HTW_CLOUD_OK == error_code) {
        return "ok";
    }
    if (HTW_CLOUD_ERR_INVALID_ARG == error_code) {
        return "invalid argument";
    }
    if (HTW_CLOUD_ERR_NOT_FOUND == error_code) {
        return "robot not found";
    }
    if (HTW_CLOUD_ERR_INTERNAL == error_code) {
        return "internal error";
    }
    return "unknown";
}

} // namespace HtwCloud
} // namespace Hantewin
