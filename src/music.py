"""High-quality procedural music generation for Tetris."""

import math
import array
import pygame


def generate_tetris_music():
    """Generate a high-quality Tetris theme with rich synthesis."""
    sample_rate = 44100

    # Tetris theme (Korobeiniki) - melody with note values
    # Format: (frequency, duration_in_beats)
    melody = [
        # First phrase
        (659, 1), (494, 0.5), (523, 0.5), (587, 1), (523, 0.5), (494, 0.5),
        (440, 1), (440, 0.5), (523, 0.5), (659, 1), (587, 0.5), (523, 0.5),
        (494, 1.5), (523, 0.5), (587, 1), (659, 1),
        (523, 1), (440, 1), (440, 1), (0, 1),
        # Second phrase
        (587, 1), (698, 0.5), (880, 1), (784, 0.5), (698, 0.5),
        (659, 1.5), (523, 0.5), (659, 1), (587, 0.5), (523, 0.5),
        (494, 1), (494, 0.5), (523, 0.5), (587, 1), (659, 1),
        (523, 1), (440, 1), (440, 1), (0, 1),
    ]

    # Bass line following the melody (root notes, one octave lower)
    bass_line = [
        # First phrase - bass plays on beats
        (165, 2), (147, 2),  # E2, D2
        (110, 2), (131, 2),  # A2, C3
        (123, 2), (147, 2),  # B2, D3
        (165, 2), (110, 2),  # E2, A2
        # Second phrase
        (147, 2), (220, 2),  # D3, A3
        (165, 2), (147, 2),  # E3, D3
        (123, 2), (147, 2),  # B2, D3
        (131, 2), (110, 2),  # C3, A2
    ]

    tempo = 140  # BPM
    beat_duration = 60.0 / tempo

    def adsr_envelope(t, duration, attack=0.01, decay=0.05, sustain=0.7, release=0.1):
        """Generate ADSR envelope value at time t."""
        if t < attack:
            # Attack phase
            return t / attack
        elif t < attack + decay:
            # Decay phase
            decay_progress = (t - attack) / decay
            return 1.0 - (1.0 - sustain) * decay_progress
        elif t < duration - release:
            # Sustain phase
            return sustain
        elif t < duration:
            # Release phase
            release_progress = (t - (duration - release)) / release
            return sustain * (1.0 - release_progress)
        return 0.0

    def generate_lead_sample(freq, t, envelope):
        """Generate lead synth sample - rich saw/triangle hybrid."""
        if freq <= 0:
            return 0.0

        # Detuned oscillators for chorus effect
        detune = 1.003

        # Triangle wave (fundamental)
        phase1 = (freq * t) % 1.0
        triangle = 4.0 * abs(phase1 - 0.5) - 1.0

        # Slightly detuned triangle
        phase2 = (freq * detune * t) % 1.0
        triangle2 = 4.0 * abs(phase2 - 0.5) - 1.0

        # Soft sawtooth for brightness
        phase3 = (freq * t) % 1.0
        saw = 2.0 * phase3 - 1.0
        # Soften the sawtooth
        saw = saw * 0.3

        # Mix oscillators
        osc = (triangle * 0.5 + triangle2 * 0.3 + saw * 0.2)

        # Add harmonics for richness
        harmonic2 = math.sin(2 * math.pi * freq * 2 * t) * 0.15
        harmonic3 = math.sin(2 * math.pi * freq * 3 * t) * 0.08

        return envelope * (osc + harmonic2 + harmonic3) * 0.4

    def generate_bass_sample(freq, t, envelope):
        """Generate bass synth sample - warm and full."""
        if freq <= 0:
            return 0.0

        # Sine wave fundamental
        sine = math.sin(2 * math.pi * freq * t)

        # Sub-octave for depth
        sub = math.sin(2 * math.pi * freq * 0.5 * t) * 0.5

        # Slight saturation/warmth
        combined = sine + sub
        # Soft clip for warmth
        if combined > 1.0:
            combined = 1.0 - (1.0 - combined) * 0.3
        elif combined < -1.0:
            combined = -1.0 - (-1.0 - combined) * 0.3

        return envelope * combined * 0.35

    def generate_drum_sample(t, beat_in_measure):
        """Generate simple drum pattern."""
        # Kick on beats 1 and 3
        kick = 0.0
        if beat_in_measure in [0, 2]:
            kick_t = t % (beat_duration * 0.5)
            if kick_t < 0.1:
                kick_freq = 80 * math.exp(-kick_t * 30)
                kick = math.sin(2 * math.pi * kick_freq * kick_t) * math.exp(-kick_t * 20) * 0.4

        # Hi-hat on off-beats
        hihat = 0.0
        if beat_in_measure in [1, 3]:
            hat_t = t % (beat_duration * 0.25)
            if hat_t < 0.03:
                # Noise-like hi-hat using multiple sine waves
                hihat = (math.sin(2 * math.pi * 8000 * hat_t) * 0.3 +
                        math.sin(2 * math.pi * 10000 * hat_t) * 0.2 +
                        math.sin(2 * math.pi * 12000 * hat_t) * 0.1)
                hihat *= math.exp(-hat_t * 150) * 0.15

        return kick + hihat

    # Calculate total duration
    total_beats = sum(beats for _, beats in melody)
    total_duration = total_beats * beat_duration
    total_samples = int(sample_rate * total_duration)

    # Pre-calculate melody timing
    melody_events = []
    current_beat = 0
    for freq, beats in melody:
        start_time = current_beat * beat_duration
        duration = beats * beat_duration
        melody_events.append((start_time, start_time + duration, freq, duration))
        current_beat += beats

    # Pre-calculate bass timing
    bass_events = []
    current_beat = 0
    for freq, beats in bass_line:
        start_time = current_beat * beat_duration
        duration = beats * beat_duration
        bass_events.append((start_time, start_time + duration, freq, duration))
        current_beat += beats

    # Generate samples
    left_samples = []
    right_samples = []

    for i in range(total_samples):
        t = i / sample_rate

        # Find current melody note
        lead = 0.0
        for start, end, freq, duration in melody_events:
            if start <= t < end:
                note_t = t - start
                env = adsr_envelope(note_t, duration, attack=0.008, decay=0.05, sustain=0.6, release=0.08)
                lead = generate_lead_sample(freq, note_t, env)
                break

        # Find current bass note
        bass = 0.0
        for start, end, freq, duration in bass_events:
            if start <= t < end:
                note_t = t - start
                env = adsr_envelope(note_t, duration, attack=0.01, decay=0.1, sustain=0.8, release=0.15)
                bass = generate_bass_sample(freq, note_t, env)
                break

        # Drums
        beat_position = t / beat_duration
        beat_in_measure = int(beat_position) % 4
        drums = generate_drum_sample(t, beat_in_measure)

        # Mix all elements
        mix = lead + bass + drums

        # Soft limiting to prevent clipping
        if mix > 0.95:
            mix = 0.95 + (mix - 0.95) * 0.1
        elif mix < -0.95:
            mix = -0.95 + (mix + 0.95) * 0.1

        # Stereo widening - slight delay and pan differences
        left = mix + lead * 0.1  # Lead slightly louder on left
        right = mix + lead * 0.08  # Slightly less on right

        # Convert to 16-bit integer
        left_sample = int(max(-32767, min(32767, left * 32767)))
        right_sample = int(max(-32767, min(32767, right * 32767)))

        left_samples.append(left_sample)
        right_samples.append(right_sample)

    # Interleave stereo samples
    stereo_samples = []
    for l, r in zip(left_samples, right_samples):
        stereo_samples.append(l)
        stereo_samples.append(r)

    # Create pygame sound from samples
    sound_array = array.array('h', stereo_samples)
    sound = pygame.mixer.Sound(buffer=sound_array)

    return sound
