/**
 * SignBridge — Milestone M3.5 / M5: American Sign Language (ASL) Translation Interface
 *
 * Implements a strict, decoupled ASL pipeline interface.
 *
 * CRITICAL LINGUISTIC & GOVERNANCE REQUIREMENTS (ADR-001, ADR-006):
 * 1. ISL and ASL are distinct, independent sign languages with different phonologies,
 *    grammars, and cultural origins.
 * 2. This module strictly isolates the ASL pipeline from the ISL pipeline.
 * 3. English word-for-word substitution is NOT sign language. We do NOT invent ASL signs
 *    or apply ISL grammar heuristics to ASL.
 * 4. Milestone M3 prioritizes ISL; full ASL lexicon and grammar are scheduled for Milestone M5.
 * 5. All unverified or unsupported words are explicitly preserved in `unsupportedWords`
 *    and emit safe neutral rest poses rather than fabricated signing.
 *
 * Architecture Convention:
 * - UMD wrapper compatible with browser extension scripts, Web Workers, and Node.js.
 * - Reuses existing contracts from `extension/models/sign_contracts.js`.
 * - Zero external runtime dependencies.
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    const contracts = require('../models/sign_contracts.js');
    module.exports = factory(contracts);
  } else if (typeof define === 'function' && define.amd) {
    define(['../models/sign_contracts.js'], factory);
  } else {
    root.SignBridgeASLTranslator = factory(root.SignBridgeContracts || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeContracts : null));
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (SignBridgeContracts) {
  'use strict';

  if (!SignBridgeContracts) {
    throw new Error('SignBridgeContracts dependency is required by ASLTranslator. Ensure sign_contracts.js is loaded first.');
  }

  const ASL_PIPELINE_STATUS = 'ASL_SCHEDULED_FOR_M5';
  const ASL_GOVERNANCE_NOTICE = 'American Sign Language (ASL) is a distinct linguistic system scheduled for Milestone M5. English word substitution is not validated ASL.';

  /**
   * ASL Seed Lexicon is intentionally empty during Milestone M3.
   * ASL lexical development is strictly segregated to Milestone M5.
   */
  const ASL_SEED_LEXICON = Object.freeze({});

  /**
   * Normalizes raw spoken transcript for ASL tokenization.
   *
   * @param {string} text - Raw input transcript.
   * @returns {{ normalizedText: string, tokens: string[] }}
   */
  function normalizeTranscript(text) {
    if (!text || typeof text !== 'string') {
      return { normalizedText: '', tokens: [] };
    }
    const clean = text
      .toLowerCase()
      .replace(/[^\w\s'-]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    const tokens = clean.length > 0 ? clean.split(' ').filter(t => t.length > 0) : [];
    return { normalizedText: clean, tokens };
  }

  /**
   * Translates a spoken English transcript into an ASL SignSequence.
   * In Milestone M3.5, this module acts as a strict architectural separation:
   * it preserves all words in `unsupportedWords`, avoids naive English substitution,
   * and creates a valid SignSequence with language: 'ASL'.
   *
   * @param {string} transcript - Input speech transcript.
   * @param {Object} [options] - Translation options and chunk metadata.
   * @returns {Readonly<Object>} Validated, immutable SignSequence.
   */
  function translateTranscriptToASL(transcript, options = {}) {
    const rawTranscript = typeof transcript === 'string' ? transcript : '';
    const { tokens } = normalizeTranscript(rawTranscript);

    const sourceChunkSeq = Number.isInteger(options.sourceChunkSeq) ? options.sourceChunkSeq : 0;
    const startMediaTimeMs = typeof options.startMediaTimeMs === 'number' && Number.isFinite(options.startMediaTimeMs)
      ? Math.max(0, options.startMediaTimeMs)
      : 0;
    const endMediaTimeMs = typeof options.endMediaTimeMs === 'number' && Number.isFinite(options.endMediaTimeMs)
      ? Math.max(startMediaTimeMs, options.endMediaTimeMs)
      : startMediaTimeMs + 2000;

    const sequenceId = typeof options.sequenceId === 'string' && options.sequenceId.trim().length > 0
      ? options.sequenceId.trim()
      : `asl_seq_${sourceChunkSeq}_${Date.now()}`;

    // All spoken tokens are honestly tracked as unsupported in M3.5 since ASL lexicon is unpopulated
    const unsupportedWords = Object.freeze([...tokens]);

    // Construct and validate complete SignSequence conforming to data contracts
    const sequence = SignBridgeContracts.createSignSequence({
      sequenceId,
      language: 'ASL',
      rawTranscript,
      sourceChunkSeq,
      startMediaTimeMs,
      endMediaTimeMs,
      signs: [], // No fabricated signs without validated ASL assets
      unsupportedWords,
      fingerspellingApplied: false
    });

    return sequence;
  }

  return Object.freeze({
    ASL_PIPELINE_STATUS,
    ASL_GOVERNANCE_NOTICE,
    ASL_SEED_LEXICON,
    normalizeTranscript,
    translateTranscriptToASL
  });
});
