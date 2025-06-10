import subprocess
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def is_ffmpeg_installed() -> bool:
    """
    Verifica si FFmpeg está disponible en el sistema.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error("FFmpeg o FFprobe no están instalados: %s", e)
        return False


def get_media_info(input_path: Path) -> dict:
    """
    Devuelve un diccionario con metadata del archivo multimedia:
      - duration (segundos)
      - format
      - streams: lista de codex, codec_type, resolution...
    """
    if not is_ffmpeg_installed():
        raise EnvironmentError("FFprobe no disponible")

    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        str(input_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    info = json.loads(result.stdout)
    # Extraer duración como float
    duration = float(info.get('format', {}).get('duration', 0.0))
    return {
        'format': info.get('format', {}).get('format_name'),
        'duration': duration,
        'size': int(info.get('format', {}).get('size', 0)),
        'streams': info.get('streams', [])
    }


def transcode_video(
    input_path: Path,
    output_path: Path,
    video_codec: str = 'libx264',
    audio_codec: str = 'aac',
    crf: int = 23,
    preset: str = 'medium',
    resolution: str = '1920x1080',
    overwrite: bool = True
) -> None:
    """
    Transcodifica un video a MP4 usando H.264 y AAC.
    - crf: calidad (18-28)
    - preset: ultrafast, superfast, veryfast, faster, fast, medium, slow...
    - resolution: WxH (p.ej. '1920x1080')
    """
    if not is_ffmpeg_installed():
        raise EnvironmentError("FFmpeg no disponible")

    cmd = [
        'ffmpeg', '-y' if overwrite else '-n',
        '-i', str(input_path),
        '-c:v', video_codec,
        '-preset', preset,
        '-crf', str(crf),
        '-vf', f"scale={resolution}",
        '-c:a', audio_codec,
        str(output_path)
    ]
    logger.info("Ejecutando transcodificación: %s", ' '.join(cmd))
    subprocess.run(cmd, check=True)


def generate_thumbnail(
    input_path: Path,
    output_path: Path,
    time_offset: float = 1.0,
    resolution: str = '640x360',
    overwrite: bool = True
) -> None:
    """
    Genera una miniatura de un video o imagen en el segundo especificado.
    - time_offset: tiempo en segundos donde capturar el frame
    - resolution: tamaño WxH de la miniatura
    """
    if not is_ffmpeg_installed():
        raise EnvironmentError("FFmpeg no disponible para thumbnails")

    cmd = [
        'ffmpeg', '-y' if overwrite else '-n',
        '-ss', str(time_offset),
        '-i', str(input_path),
        '-vframes', '1',
        '-vf', f"scale={resolution}:force_original_aspect_ratio=decrease",
        str(output_path)
    ]
    logger.info("Generando thumbnail: %s", ' '.join(cmd))
    subprocess.run(cmd, check=True)


def transcode_to_hls(
    input_path: Path,
    output_dir: Path,
    playlist_name: str = 'playlist.m3u8',
    segment_time: int = 6,
    resolution: str = '1920x1080'
) -> None:
    """
    Transcodifica un video en HLS (segmentos .ts y archivo .m3u8).
    - segment_time: duración de cada segmento en segundos
    - resolution: resolución de salida
    """
    if not is_ffmpeg_installed():
        raise EnvironmentError("FFmpeg no disponible para HLS")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_playlist = output_dir / playlist_name

    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_path),
        '-c:v', 'libx264',
        '-vf', f"scale={resolution}",
        '-c:a', 'aac',
        '-hls_time', str(segment_time),
        '-hls_list_size', '0',
        '-hls_segment_filename', str(output_dir / 'seg_%03d.ts'),
        str(output_playlist)
    ]
    logger.info("Transcodificando a HLS: %s", ' '.join(cmd))
    subprocess.run(cmd, check=True)
