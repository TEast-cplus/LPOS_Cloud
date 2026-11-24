/**
 * @file error_code.h
 * @brief HTW Cloud protocol error codes (placeholder)
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

#ifndef HTWCLOUD_ERROR_CODE_H
#define HTWCLOUD_ERROR_CODE_H

namespace Hantewin {
namespace HtwCloud {

/**
 * @brief Cloud protocol / API error codes
 * @date 2026-11-24
 * @author HTW_DEV
 */
typedef enum {
    HTW_CLOUD_OK = 0,
    HTW_CLOUD_ERR_INVALID_ARG = 1,
    HTW_CLOUD_ERR_NOT_FOUND = 40401,
    HTW_CLOUD_ERR_INTERNAL = 50000
} HTW_CLOUD_ERROR_E;

/**
 * @brief Convert error code to short English message
 * @param error_code Error enumeration value
 * @return Non-owning C string
 */
const char* errorCodeToString(HTW_CLOUD_ERROR_E error_code);

} // namespace HtwCloud
} // namespace Hantewin

#endif // HTWCLOUD_ERROR_CODE_H
