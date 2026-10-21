/**
 * SignBridge — Milestone M3 Phase 3.1: Data Contracts Specification
 *
 * Implements pure, zero-dependency data contracts, strict schema validation,
 * and immutable factory builders for SignItem and SignSequence objects.
 *
 * CRITICAL SPECIFICATIONS & ARCHITECTURAL DECISIONS (ADR-010):
 * 1. SignItem and SignSequence contracts are pure, zero-dependency JavaScript objects.
 * 2. Implements UMD module wrapper supporting Browser globals (window.SignBridgeContracts),
 *    CommonJS (module.exports / require), and AMD (define).
 * 3. Enforces strict validation:
 *    - gloss: non-empty uppercase alphanumeric string format (e.g. "HELLO", "THANK_YOU").
 *    - category: 'lexical' | 'fingerspelling' | 'pause'
 *    - source: 'seed_dictionary' | 'fingerspell_fallback' | 'grammar_pause'
 *    - durationMs: non-negative finite number.
 *    - animationId: nullable/optional string matching /^[a-zA-Z0-9_.-]+$/. Decouples linguistic
 *      translation from downstream physical keyframe asset registry.
 *    - nonManualMarker: optional object with headTilt and eyebrows enum values.
 *    - Category & source consistency: 'fingerspelling' requires 'fingerspell_fallback';
 *      'pause' requires 'grammar_pause'; 'lexical' requires 'seed_dictionary'.
 *    - Single-character gloss constraint: 'fingerspelling' category requires a single-character gloss (A-Z).
 *    - language: 'ISL' | 'ASL'
 *    - startMediaTimeMs & endMediaTimeMs: non-negative finite numbers with endMediaTimeMs >= startMediaTimeMs.
 *    - unsupportedWords: array of non-empty strings (honest reporting; no phantom signs).
 *    - fingerspellingApplied: boolean flag.
 * 4. Immutability: Factory functions (createSignItem, createSignSequence) freeze return objects
 *    and nested arrays (Object.freeze) to guarantee that queued sign sequences cannot be mutated mid-playback.
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    module.exports = factory();
  } else if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else {
    root.SignBridgeContracts = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const CONTRACT_VERSION = '1.0.0';

  /**
   * Allowed enum values.
   */
  const CATEGORIES = Object.freeze(['lexical', 'fingerspelling', 'pause']);
  const SOURCES = Object.freeze(['seed_dictionary', 'fingerspell_fallback', 'grammar_pause']);
  const LANGUAGES = Object.freeze(['ISL', 'ASL']);
  const HEAD_TILTS = Object.freeze(['left', 'right', 'forward', 'none']);
  const EYEBROWS = Object.freeze(['raised', 'furrowed', 'neutral']);

  const ANIMATION_ID_PATTERN = /^[a-zA-Z0-9_.-]+$/;
  const GLOSS_FORMAT_PATTERN = /^[A-Z0-9_-]+$/;

  /**
   * Custom Contract Validation Error
   */
  class ContractValidationError extends Error {
    constructor(message, errors = []) {
      super(message);
      this.name = 'ContractValidationError';
      this.errors = errors;
    }
  }

  /**
   * Validates an individual SignItem object against Milestone M3 contracts.
   *
   * @param {Object} item - Candidate SignItem.
   * @returns {{ valid: boolean, errors: string[] }}
   */
  function validateSignItem(item) {
    const errors = [];

    if (!item || typeof item !== 'object' || Array.isArray(item)) {
      return { valid: false, errors: ['SignItem must be a non-null object'] };
    }

    // 1. gloss validation
    if (!('gloss' in item) || typeof item.gloss !== 'string' || item.gloss.trim().length === 0) {
      errors.push("SignItem requires a valid non-empty gloss string");
    } else {
      const trimmed = item.gloss.trim();
      if (trimmed !== trimmed.toUpperCase() || !GLOSS_FORMAT_PATTERN.test(trimmed)) {
        errors.push("SignItem gloss must be in uppercase alphanumeric format");
      }
      if (item.category === 'fingerspelling') {
        if (trimmed.length !== 1) {
          errors.push("Category 'fingerspelling' requires a single-character gloss (A-Z)");
        }
      }
    }

    // 2. category validation
    if (!('category' in item)) {
      errors.push("SignItem requires a category property");
    } else if (!CATEGORIES.includes(item.category)) {
      errors.push(`Invalid SignItem category '${item.category}'. Allowed categories: [${CATEGORIES.join(', ')}]`);
    }

    // 3. durationMs validation
    if (!('durationMs' in item)) {
      errors.push("SignItem requires a durationMs property");
    } else if (typeof item.durationMs !== 'number' || !Number.isFinite(item.durationMs) || item.durationMs < 0) {
      errors.push("SignItem durationMs must be a non-negative finite number");
    }

    // 4. source validation
    if (!('source' in item)) {
      errors.push("SignItem requires a source property in direct validator");
    } else if (!SOURCES.includes(item.source)) {
      errors.push(`Invalid SignItem source '${item.source}'. Allowed sources: [${SOURCES.join(', ')}]`);
    }

    // 5. category and source consistency
    if (item.category === 'fingerspelling' && item.source !== 'fingerspell_fallback') {
      errors.push("Category 'fingerspelling' must have source 'fingerspell_fallback'");
    }
    if (item.category === 'pause' && item.source !== 'grammar_pause') {
      errors.push("Category 'pause' must have source 'grammar_pause'");
    }
    if (item.category === 'lexical' && item.source && item.source !== 'seed_dictionary') {
      errors.push("Category 'lexical' must have source 'seed_dictionary'");
    }

    // 6. animationId validation (optional / nullable)
    if (item.animationId !== undefined && item.animationId !== null) {
      if (typeof item.animationId !== 'string' || !ANIMATION_ID_PATTERN.test(item.animationId)) {
        errors.push("SignItem animationId must be a valid string matching /^[a-zA-Z0-9_.-]+$/");
      }
    }

    // 7. nonManualMarker validation (optional)
    if (item.nonManualMarker !== undefined && item.nonManualMarker !== null) {
      if (typeof item.nonManualMarker !== 'object' || Array.isArray(item.nonManualMarker)) {
        errors.push("SignItem nonManualMarker must be an object");
      } else {
        if (item.nonManualMarker.headTilt !== undefined && !HEAD_TILTS.includes(item.nonManualMarker.headTilt)) {
          errors.push(`Invalid headTilt value '${item.nonManualMarker.headTilt}'. Allowed: [${HEAD_TILTS.join(', ')}]`);
        }
        if (item.nonManualMarker.eyebrows !== undefined && !EYEBROWS.includes(item.nonManualMarker.eyebrows)) {
          errors.push(`Invalid eyebrows value '${item.nonManualMarker.eyebrows}'. Allowed: [${EYEBROWS.join(', ')}]`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Factory function that constructs and freezes an immutable SignItem.
   *
   * @param {Object} data - Initial SignItem data.
   * @returns {Readonly<Object>} Frozen SignItem.
   */
  function createSignItem(data = {}) {
    const rawGloss = (data && typeof data.gloss === 'string') ? data.gloss.trim() : '';
    const gloss = rawGloss.toUpperCase();
    const category = (data && data.category) || 'lexical';
    const source = (data && data.source) || (
      category === 'fingerspelling'
        ? 'fingerspell_fallback'
        : (category === 'pause' ? 'grammar_pause' : 'seed_dictionary')
    );
    const durationMs = (data && typeof data.durationMs === 'number' && Number.isFinite(data.durationMs))
      ? data.durationMs
      : 500;
    const animationId = (data && data.animationId !== undefined && data.animationId !== '')
      ? data.animationId
      : null;

    const item = {
      gloss,
      category,
      durationMs,
      source,
      animationId
    };

    if (data && data.nonManualMarker && typeof data.nonManualMarker === 'object') {
      const nmm = {};
      if (data.nonManualMarker.headTilt !== undefined) nmm.headTilt = data.nonManualMarker.headTilt;
      if (data.nonManualMarker.eyebrows !== undefined) nmm.eyebrows = data.nonManualMarker.eyebrows;
      item.nonManualMarker = Object.freeze(nmm);
    }

    return Object.freeze(item);
  }

  /**
   * Validates a complete SignSequence object against Milestone M3 contracts.
   *
   * @param {Object} seq - Candidate SignSequence.
   * @returns {{ valid: boolean, errors: string[] }}
   */
  function validateSignSequence(seq) {
    const errors = [];

    if (!seq || typeof seq !== 'object' || Array.isArray(seq)) {
      return { valid: false, errors: ['SignSequence must be a non-null object'] };
    }

    // 1. sequenceId
    if (!('sequenceId' in seq) || typeof seq.sequenceId !== 'string' || seq.sequenceId.trim().length === 0) {
      errors.push("SignSequence requires a non-empty sequenceId string");
    }

    // 2. language
    if (!('language' in seq)) {
      errors.push("SignSequence requires a language property");
    } else if (!LANGUAGES.includes(seq.language)) {
      errors.push(`Invalid SignSequence language '${seq.language}'. Allowed: [${LANGUAGES.join(', ')}]`);
    }

    // 3. rawTranscript
    if ('rawTranscript' in seq && typeof seq.rawTranscript !== 'string') {
      errors.push("SignSequence rawTranscript must be a string");
    }

    // 4. sourceChunkSeq
    if ('sourceChunkSeq' in seq && (!Number.isInteger(seq.sourceChunkSeq) || seq.sourceChunkSeq < 0)) {
      errors.push("SignSequence sourceChunkSeq must be a non-negative integer");
    }

    // 5. startMediaTimeMs
    if (!('startMediaTimeMs' in seq) || typeof seq.startMediaTimeMs !== 'number' || !Number.isFinite(seq.startMediaTimeMs) || seq.startMediaTimeMs < 0) {
      errors.push("SignSequence startMediaTimeMs must be a non-negative finite number");
    }

    // 6. endMediaTimeMs
    if (!('endMediaTimeMs' in seq) || typeof seq.endMediaTimeMs !== 'number' || !Number.isFinite(seq.endMediaTimeMs)) {
      errors.push("SignSequence endMediaTimeMs must be a finite number");
    } else if (typeof seq.startMediaTimeMs === 'number' && Number.isFinite(seq.startMediaTimeMs) && seq.endMediaTimeMs < seq.startMediaTimeMs) {
      errors.push("SignSequence endMediaTimeMs must be greater than or equal to startMediaTimeMs");
    }

    // 7. signs array & nested children validation
    if (!('signs' in seq) || !Array.isArray(seq.signs)) {
      errors.push("SignSequence requires a signs array");
    } else {
      seq.signs.forEach((item, index) => {
        const itemRes = validateSignItem(item);
        if (!itemRes.valid) {
          itemRes.errors.forEach(err => {
            errors.push(`signs[${index}]: ${err}`);
          });
        }
      });
    }

    // 8. unsupportedWords
    if (!('unsupportedWords' in seq) || !Array.isArray(seq.unsupportedWords)) {
      errors.push("SignSequence requires an unsupportedWords array");
    } else {
      seq.unsupportedWords.forEach((word, index) => {
        if (typeof word !== 'string' || word.trim().length === 0) {
          errors.push(`unsupportedWords[${index}] must be a non-empty string`);
        }
      });
    }

    // 9. fingerspellingApplied
    if (!('fingerspellingApplied' in seq)) {
      errors.push("SignSequence requires a fingerspellingApplied boolean property");
    } else if (typeof seq.fingerspellingApplied !== 'boolean') {
      errors.push("SignSequence fingerspellingApplied must be a boolean");
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Factory function that constructs and freezes an immutable SignSequence.
   *
   * @param {Object} data - Initial SignSequence data.
   * @returns {Readonly<Object>} Frozen SignSequence.
   */
  function createSignSequence(data = {}) {
    const sequenceId = (data && typeof data.sequenceId === 'string' && data.sequenceId.trim().length > 0)
      ? data.sequenceId.trim()
      : `seq_${Date.now()}`;

    const language = (data && typeof data.language === 'string' && data.language.trim().length > 0)
      ? data.language.trim().toUpperCase()
      : 'ISL';

    const rawTranscript = (data && typeof data.rawTranscript === 'string')
      ? data.rawTranscript
      : '';

    const sourceChunkSeq = (data && Number.isInteger(data.sourceChunkSeq))
      ? data.sourceChunkSeq
      : 0;

    const startMediaTimeMs = (data && typeof data.startMediaTimeMs === 'number' && Number.isFinite(data.startMediaTimeMs))
      ? Math.max(0, data.startMediaTimeMs)
      : 0;

    const endMediaTimeMs = (data && typeof data.endMediaTimeMs === 'number' && Number.isFinite(data.endMediaTimeMs))
      ? Math.max(startMediaTimeMs, data.endMediaTimeMs)
      : startMediaTimeMs;

    const rawSigns = (data && Array.isArray(data.signs)) ? data.signs : [];
    const signs = rawSigns.map(s => {
      if (s && Object.isFrozen(s) && validateSignItem(s).valid) {
        return s;
      }
      return createSignItem(s);
    });

    const rawUnsupported = (data && Array.isArray(data.unsupportedWords)) ? data.unsupportedWords : [];
    const unsupportedWords = rawUnsupported.map(w => (typeof w === 'string' ? w : String(w)));

    const fingerspellingApplied = Boolean(data && data.fingerspellingApplied);

    const seq = {
      sequenceId,
      language,
      rawTranscript,
      sourceChunkSeq,
      startMediaTimeMs,
      endMediaTimeMs,
      signs: Object.freeze(signs),
      unsupportedWords: Object.freeze(unsupportedWords),
      fingerspellingApplied
    };

    if (data && typeof data.grammarApplied === 'boolean') {
      seq.grammarApplied = data.grammarApplied;
    }

    return Object.freeze(seq);
  }

  return Object.freeze({
    CONTRACT_VERSION,
    CATEGORIES,
    SOURCES,
    LANGUAGES,
    HEAD_TILTS,
    EYEBROWS,
    ContractValidationError,
    validateSignItem,
    validateSignSequence,
    createSignItem,
    createSignSequence
  });
});
