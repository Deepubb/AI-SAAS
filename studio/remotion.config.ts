import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(95);
Config.setCodec("h264");
Config.setCrf(16);
Config.setPixelFormat("yuv420p");
// Tagged BT.709 limited range: plays consistently on phones and survives Instagram transcoding.
Config.setColorSpace("bt709");
Config.setAudioBitrate("320k");
Config.setOverwriteOutput(true);
// Use a preinstalled Chrome Headless Shell when Remotion can't download its own.
Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE ?? null);
