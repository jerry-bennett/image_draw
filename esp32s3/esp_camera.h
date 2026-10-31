// esp_camera.h - Full ESP32 Camera Driver Header (Arduino-compatible)
// Based on ESP-IDF camera driver but adapted for Arduino

#ifndef _ESP_CAMERA_H_
#define _ESP_CAMERA_H_

#include <Arduino.h>

// ============================================================================
// Type Definitions (from esp-camera-drv/esp_cam/types.h)
// ============================================================================

#ifdef __cplusplus
extern "C" {
#endif

typedef struct camera_xclk_cfg_t {
  uint32_t freq_hz;
  int8_t ledc_timer, pin;
} camera_xclk_cfg_t;

typedef struct camera_i2s_cfg_t {
  int8_t sba_pin, bck_pin, lclk_pin, din_pin, dout_pin;
} camera_i2s_cfg_t;

typedef enum {
    CAMERA_I2S_CFG_AUTO = -1
} camera_i2s_mode_t;

typedef struct camera_mipi_dphy_cfg_t {
  int8_t pad0, pad1, pad2, pad3, pad4, pad5, pad6, pad7;
  int8_t pad_hsi, pad_pclk, clk_ext_enabled;
} camera_mipi_dphy_cfg_t;

typedef struct camera_mipi_sensor_cfg_t {
  uint32_t clock_freq_khz;
  camera_xclk_cfg_t xclk;
} camera_mipi_sensor_cfg_t;

typedef enum {
    MIPI_FMT_RGB565LSB = 0,
    MIPI_FMT_BGR565,
    MIPI_FMT_YUYV
} camera_mipi_format_t;

typedef struct camera_mipi_config_t {
  camera_mipi_dphy_cfg_t dphy;
  int8_t csi_pclk_freq_mhz;
  uint32_t clock_div;
  int8_t lane_switch_enable;
  int8_t lane_lane0, lane_lane1, lane_lane2, lane_lane3;
  camera_i2s_cfg_t sba;
  camera_i2s_mode_t mode;
  camera_mipi_format_t fmt;
  camera_mipi_sensor_cfg_t sensor;
} camera_mipi_config_t;

typedef struct camera_vsync_cfg_t {
  int8_t pad, hblank_start, hblank_end, vblank_start, vblank_end;
} camera_vsync_cfg_t;

typedef enum {
    CSI_FMT_RGB565LSB = 0,
    CSI_FMT_BGR565,
    CSI_FMT_YUYV
} camera_csi_format_t;

typedef struct camera_csi_config_t {
  int8_t pclk_freq_mhz;
  uint32_t clock_div;
  int8_t vflip, hflip;
  camera_vsync_cfg_t vsync;
  camera_i2s_cfg_t sba;
  camera_i2s_mode_t mode;
  camera_csi_format_t fmt;
  int8_t pad0, pad1, pad2, pad3, pad4, pad5, pad6, pad7;
} camera_csi_config_t;

typedef struct {
    int8_t fps;
    uint32_t frame_rate_limit;
    camera_i2s_cfg_t sba;
    int8_t sba_mode;
    int8_t hsync_deassert_us;
    int8_t vsync_deassert_us;
} camera_stream_cfg_t;

typedef struct {
    enum esp_vsync_polarity_type {
        ESP_VSYNC_POLARITY_LOW,
        ESP_VSYNC_POLARITY_HIGH,
    } vsync_polarity;

    int8_t fps, frame_rate_limit;
    bool enabled;
} camera_stream_cfg_t;

typedef struct {
  int8_t pad0, pad1, pad2, pad3, pad4, pad5, pad6, pad7;
  uint32_t hblank_start_us, hblank_end_us;
  uint32_t vsync_start_us, vsync_end_us;
  camera_i2s_cfg_t sba;
  int8_t sba_mode;
  int8_t hsync_deassert_us;
  int8_t vsync_deassert_us;
} camera_stream_cfg_t;

typedef enum {
    PIXFORMAT_RGB565 = 0,
    PIXFORMAT_YUV422,
    PIXFORMAT_JPEG
} pixel_format_t;

typedef enum {
    FRAMESIZE_QVGA = 320 * 240,   // VGA (640x480)
    FRAMESIZE_VGA = 640 * 480,
    FRAMESIZE_SVGA = 800 * 600,
    FRAMESIZE_XGA = 1024 * 768,
    FRAMESIZE_UXGA = 1280 * 1024, // Minimum for OV5640 AF
    FRAMESIZE_4M = 1920 * 1080,
    FRAMESIZE_FULL = 2560 * 1440,
    FRAMESIZE_SXGA = 1408 * 1088,
    FRAMESIZE_QXGA = 2048 * 1536,
    FRAMESIZE_UHD = 3840 * 2160
} frame_size_t;

typedef struct {
  int x, y;
} coord_t;

typedef enum {
    ESP_CAMERA_PAL_NTSC = 0,   // North America and Japan
    ESP_CAMERA_PAL_50Hz        // Europe, Australia, Africa, South America
} esp_camera_std_t;

typedef enum {
    CAMERA_STUB = 0,
    CAMERA_PREVIEW = 1,
    CAMERA_BW = 2,
    CAMERA_JPEG = 3,
    CAMERA_STREAM = 4,
    ESP_CAMERA_RAW = 5,         // Raw data with no processing.
    ESP_CAMERA_RAW_WFOCUS        // Raw data with focus processing
} camera_mode_t;

typedef struct {
  uint8_t id[10];              // sensor ID
  const char *model;           // sensor model name
  uint32_t fps_max;            // maximum FPS (in Hz)
  frame_size_t framesize_max;  // max supported resolution/frame size
  int8_t jpeg_quality_min, jpeg_quality_max;      // JPEG quality range [0..63]
  esp_camera_std_t pixel_std;  // NTSC or PAL (not all sensors support this)
  uint8_t id_v2[10];           // sensor ID v2 for newer ESP32 cameras
  int xclk_freq_hz;            // clock frequency in Hz (may be overwritten by camera init)
  frame_size_t framesize;      // recommended resolution/frame size
  pixel_format_t pixel_fmt;    // pixel format (RGB565/YUV422/JPEG)
  bool raw_buf;                // raw buffer mode (raw capture)
  uint16_t raw_buffer_size;    // raw buffer size in bytes
  int fb_location;             // memory location for frame buffer (CAMERA_FB_IN_PSRAM or CAMERA_FB_IN_DRAM)
} sensor_t;

typedef struct {
  camera_xclk_cfg_t xclk;                    // clock configuration
  frame_size_t framesize;                     // resolution/frame size
  pixel_format_t pixel_format;                // pixel format (RGB565/YUV422/JPEG)
  int jpeg_quality;                           // JPEG quality [0..63]
  camera_stream_cfg_t streamcfg;              // stream configuration
  bool raw_buf;                               // raw buffer mode (raw capture)
  uint16_t raw_buffer_size;                   // raw buffer size in bytes
  sensor_t *sensor;                           // sensor handle
  bool led_trigger;                           // trigger LED
  camera_mode_t mode;                         // camera mode
} camera_config_t;

// ============================================================================
// ESP32 Pin Definitions for XIAO ESP32-S3 Sense (OV5640)
// ============================================================================

#define XCLK_GPIO_NUM           10
#define Y9_GPIO_NUM             48  // DVP_Y9
#define Y8_GPIO_NUM             11  // D7 (DVP_Y8)
#define PCLK_GPIO_NUM           13  // D5 (DVP_PCLK)
#define Y7_GPIO_NUM             12  // D6 (DVP_Y7)
#define Y6_GPIO_NUM             14  // D4 (DVP_Y6)
#define Y5_GPIO_NUM             16  // D2 (DVP_Y5)
#define Y4_GPIO_NUM             18  // D0 (DVP_Y4)
#define Y3_GPIO_NUM             17  // D1 (DVP_Y3)
#define Y2_GPIO_NUM             15  // D3 (DVP_Y2)
#define VSYNC_GPIO_NUM          38
#define HREF_GPIO_NUM           47
#define SIOD_GPIO_NUM           39  // SDA (I2C data)
#define SIOC_GPIO_NUM           40  // SCL (I2C clock)

// ============================================================================
// ESP32 Camera Driver API
// ============================================================================

esp_err_t esp_camera_init(camera_config_t *cfg);
void esp_camera_reset();

// Get the current sensor handle
sensor_t *esp_camera_sensor_get();

// Get camera status
bool get_camera_status();

// Capture a frame buffer (must return immediately if no capture)
camera_fb_t *esp_camera_fb_get();

// Release frame buffer and optionally save to file
void esp_camera_fb_return(camera_fb_t *fb);
void esp_camera_fb_save(FILE *fs, const char *fileName, camera_fb_t *fb);

// Get sensor info
sensor_info_t get_sensor_info(const sensor_t *s);

#ifdef __cplusplus
}
#endif

#endif // _ESP_CAMERA_H_
