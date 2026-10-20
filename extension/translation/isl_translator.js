/**
 * SignBridge — Milestone M3 Phase 3.2: Experimental Rule-Based ISL Text-to-Gloss Translator
 *
 * Implements pure, modular text normalization, tokenization, seed lexicon matching,
 * isolated experimental grammar heuristics, and honest unsupported-word reporting.
 *
 * CRITICAL LINGUISTIC & ARCHITECTURAL DISCLAIMER:
 * 1. This module is an experimental prototype for Milestone M3 engineering evaluation.
 * 2. It does NOT claim to produce fluent, natural, or linguistically authoritative Indian Sign Language (ISL).
 * 3. Text glossing (converting spoken English words into uppercase tokens) is a working engineering model,
 *    not sign language. Real ISL incorporates complex spatial syntax, classifier predicates, and
 *    grammatical facial expressions (non-manual markers).
 * 4. Finding a matching gloss token does NOT mean a sign was animated or played. No 3D animation playback exists yet.
 * 5. Words not present in the seed lexicon are explicitly preserved in `unsupportedWords`.
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
    root.SignBridgeISLTranslator = factory(root.SignBridgeContracts || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeContracts : null));
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (SignBridgeContracts) {
  'use strict';

  if (!SignBridgeContracts) {
    throw new Error('SignBridgeContracts dependency is required by ISLTranslator. Ensure sign_contracts.js is loaded first.');
  }

  // =========================================================================
  // 1. The 15 Approved Seed Lexicon Entries (ISLRTC Aligned)
  // =========================================================================

  /**
   * Bounded seed vocabulary for M3 prototype.
   * Every entry represents a verified standard conversational token.
   * Lemmas are lower-case variants mapped to the canonical uppercase gloss.
   */
  const SEED_LEXICON = Object.freeze({
    NAMASTE: Object.freeze({
      gloss: 'NAMASTE',
      category: 'lexical',
      defaultDurationMs: 1800,
      animationId: 'isl_namaste_godl_v1',
      lemmas: Object.freeze(['namaste', 'namaskar', 'namaskaram']),
      description: 'Two-handed greeting: palms pressed flat together at center chest (Anjali Mudra), slight respectful head bow (ISLRTC Vol 1, Word #0001, GODL License)',
      nonManualMarker: Object.freeze({ headTilt: 'forward', eyebrows: 'neutral' })
    }),
    HELLO: Object.freeze({
      gloss: 'HELLO',
      category: 'lexical',
      defaultDurationMs: 700,
      lemmas: Object.freeze(['hello', 'hi', 'hey', 'greetings']),
      description: 'Open flat hand raised to temple/chest, gentle outward forward arc'
    }),
    THANK_YOU: Object.freeze({
      gloss: 'THANK_YOU',
      category: 'lexical',
      defaultDurationMs: 800,
      lemmas: Object.freeze(['thank you', 'thanks', 'thank']),
      description: 'Flat dominant hand touching chin/lips, moving downward and forward'
    }),
    PLEASE: Object.freeze({
      gloss: 'PLEASE',
      category: 'lexical',
      defaultDurationMs: 700,
      lemmas: Object.freeze(['please']),
      description: 'Flat open hand rubbing clockwise over center of chest'
    }),
    WELCOME: Object.freeze({
      gloss: 'WELCOME',
      category: 'lexical',
      defaultDurationMs: 750,
      lemmas: Object.freeze(['welcome']),
      description: 'Both open hands held forward palms up, drawn smoothly toward body'
    }),
    SORRY: Object.freeze({
      gloss: 'SORRY',
      category: 'lexical',
      defaultDurationMs: 700,
      lemmas: Object.freeze(['sorry', 'apologize', 'apology']),
      description: 'Closed dominant fist rubbing circular on chest'
    }),
    YES: Object.freeze({
      gloss: 'YES',
      category: 'lexical',
      defaultDurationMs: 600,
      lemmas: Object.freeze(['yes', 'yeah', 'yep', 'correct', 'agree']),
      description: 'Dominant fist nodding downward at wrist'
    }),
    NO: Object.freeze({
      gloss: 'NO',
      category: 'lexical',
      defaultDurationMs: 600,
      lemmas: Object.freeze(['no', 'not', 'never', 'nope']),
      description: 'Dominant index finger wagging side-to-side'
    }),
    NAME: Object.freeze({
      gloss: 'NAME',
      category: 'lexical',
      defaultDurationMs: 700,
      lemmas: Object.freeze(['name', 'named', 'called']),
      description: 'Dominant H-hand tapping non-dominant H-hand'
    }),
    YOU: Object.freeze({
      gloss: 'YOU',
      category: 'lexical',
      defaultDurationMs: 500,
      lemmas: Object.freeze(['you', 'your', 'yours']),
      description: 'Dominant index finger pointing forward toward addressee'
    }),
    I: Object.freeze({
      gloss: 'I',
      category: 'lexical',
      defaultDurationMs: 500,
      lemmas: Object.freeze(['i', 'me', 'my', 'mine', 'myself']),
      description: 'Dominant index finger pointing toward center of signer chest'
    }),
    HELP: Object.freeze({
      gloss: 'HELP',
      category: 'lexical',
      defaultDurationMs: 750,
      lemmas: Object.freeze(['help', 'assist', 'assistance']),
      description: 'Closed dominant fist resting on open flat non-dominant palm'
    }),
    GOOD: Object.freeze({
      gloss: 'GOOD',
      category: 'lexical',
      defaultDurationMs: 600,
      lemmas: Object.freeze(['good', 'fine', 'well', 'great']),
      description: 'Dominant thumb-up fist moving forward'
    }),
    BAD: Object.freeze({
      gloss: 'BAD',
      category: 'lexical',
      defaultDurationMs: 600,
      lemmas: Object.freeze(['bad', 'poor', 'wrong']),
      description: 'Dominant pinky extended or hand turned palm down with downward thrust'
    }),
    STOP: Object.freeze({
      gloss: 'STOP',
      category: 'lexical',
      defaultDurationMs: 600,
      lemmas: Object.freeze(['stop', 'halt', 'cease']),
      description: 'Open flat dominant hand coming down sharply onto open non-dominant palm'
    }),
    WAIT: Object.freeze({
      gloss: 'WAIT',
      category: 'lexical',
      defaultDurationMs: 700,
      lemmas: Object.freeze(['wait', 'hold']),
      description: 'Open hands held outward at waist height, fingers fluttering'
    })
  });

  // Fast reverse lookup table for single-word lemmas
  const SINGLE_WORD_LOOKUP = new Map();
  // Multi-word phrases (e.g. "thank you") stored in descending order of length
  const MULTI_WORD_ENTRIES = [];

  for (const [glossKey, entry] of Object.entries(SEED_LEXICON)) {
    for (const lemma of entry.lemmas) {
      if (lemma.includes(' ')) {
        MULTI_WORD_ENTRIES.push({ phrase: lemma, entry });
      } else {
        SINGLE_WORD_LOOKUP.set(lemma, entry);
      }
    }
  }

  // Sort multi-word entries longest first for greedy matching
  MULTI_WORD_ENTRIES.sort((a, b) => b.phrase.length - a.phrase.length);

  // Auxiliary verbs identified for experimental heuristic elimination
  const AUXILIARY_VERBS = Object.freeze(new Set([
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being'
  ]));

  // English articles that have no ISL equivalent
  const ARTICLES = Object.freeze(new Set(['a', 'an', 'the']));

  // Temporal adverbs for experimental fronting
  const TEMPORAL_MARKERS = Object.freeze(new Set([
    'yesterday', 'today', 'tomorrow', 'now', 'morning', 'night', 'soon', 'later'
  ]));

  // WH-Question words for experimental terminal positioning
  const QUESTION_WORDS = Object.freeze(new Set([
    'what', 'why', 'when', 'where', 'who', 'how', 'which'
  ]));

  // =========================================================================
  // 2. Normalization & Tokenization
  // =========================================================================

  /**
   * Normalizes spoken transcript by stripping punctuation, trimming,
   * converting to lower-case, and extracting clean word tokens.
   *
   * @param {string} text - Raw input transcript.
   * @returns {{ normalizedText: string, tokens: string[], isQuestion: boolean }}
   */
  function normalizeTranscript(text) {
    if (typeof text !== 'string') return { normalizedText: '', tokens: [], isQuestion: false };

    const trimmed = text.trim();
    if (!trimmed) return { normalizedText: '', tokens: [], isQuestion: false };

    const isQuestion = trimmed.includes('?');

    // Replace all punctuation with spaces, keeping alphanumeric and apostrophes inside words
    const cleaned = trimmed
      .toLowerCase()
      .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'–—]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    if (!cleaned) return { normalizedText: '', tokens: [], isQuestion };

    const tokens = cleaned.split(' ').filter(t => t.length > 0);
    return { normalizedText: cleaned, tokens, isQuestion };
  }

  // =========================================================================
  // 3. Isolated Experimental Grammar Heuristics
  // =========================================================================

  /**
   * Experimental rule-based grammar transformation for ISL.
   * 
   * CAVEAT: This is an isolated heuristic approximation for pipeline prototyping.
   * It does NOT produce authoritative or fluent ISL.
   *
   * Transformations applied:
   * 1. Elimination of English auxiliary verbs (is, am, are, was, were) and articles (a, an, the).
   * 2. Fronting of temporal adverbs (e.g. "today", "yesterday") to the beginning.
   * 3. Shifting of WH-question words ("what", "where", "why") to the end.
   * 4. Basic Subject-Verb-Object (SVO) -> Subject-Object-Verb (SOV) reordering for 3-token phrases.
   *
   * @param {string[]} tokens - Normalized word tokens.
   * @param {Object} [options]
   * @param {boolean} [options.isQuestion=false] - Whether original transcript was a question.
   * @returns {string[]} Transformed token list.
   */
  function applyExperimentalGrammarHeuristics(tokens, options = {}) {
    if (!Array.isArray(tokens) || tokens.length === 0) return [];

    // Filter out auxiliary verbs and articles
    const contentTokens = tokens.filter(t => !AUXILIARY_VERBS.has(t) && !ARTICLES.has(t));
    if (contentTokens.length <= 1) return contentTokens;

    const timeTokens = [];
    const questionTokens = [];
    const coreTokens = [];

    for (const token of contentTokens) {
      if (TEMPORAL_MARKERS.has(token)) {
        timeTokens.push(token);
      } else if (QUESTION_WORDS.has(token)) {
        questionTokens.push(token);
      } else {
        coreTokens.push(token);
      }
    }

    // Basic experimental SVO -> SOV reordering on simple 3-word core patterns
    // e.g. ["i", "help", "you"] -> ["i", "you", "help"]
    if (coreTokens.length === 3) {
      const [subj, verb, obj] = coreTokens;
      const isSubjPronoun = ['i', 'you', 'he', 'she', 'we', 'they'].includes(subj);
      const isObjPronoun = ['you', 'me', 'him', 'her', 'us', 'them'].includes(obj);
      if (isSubjPronoun || isObjPronoun) {
        coreTokens[1] = obj;
        coreTokens[2] = verb;
      }
    }

    // Assemble: Time markers first + Core tokens + Question words at terminus
    return [...timeTokens, ...coreTokens, ...questionTokens];
  }

  // =========================================================================
  // 4. Seed Lexicon Matching & Unsupported Word Categorization
  // =========================================================================

  /**
   * Matches tokens against the seed lexicon with multi-word phrase priority.
   * Unmatched tokens are recorded in `unsupportedWords`.
   *
   * @param {string[]} tokens - Token list.
   * @param {Object} [options]
   * @param {boolean} [options.enableFingerspellingFallback=false] - Whether to expand unsupported words into A-Z letters.
   * @returns {{ signs: Object[], unsupportedWords: string[], fingerspellingApplied: boolean }}
   */
  function matchTokensToSeedLexicon(tokens, options = {}) {
    const signs = [];
    const unsupportedWords = [];
    let fingerspellingApplied = false;

    if (!Array.isArray(tokens) || tokens.length === 0) {
      return { signs, unsupportedWords, fingerspellingApplied };
    }

    const textToMatch = tokens.join(' ');
    let i = 0;

    while (i < tokens.length) {
      let matched = false;

      // Check multi-word entries first (e.g. "thank you")
      for (const { phrase, entry } of MULTI_WORD_ENTRIES) {
        const phraseTokens = phrase.split(' ');
        const phraseLen = phraseTokens.length;

        if (i + phraseLen <= tokens.length) {
          const slice = tokens.slice(i, i + phraseLen).join(' ');
          if (slice === phrase) {
            const signObj = {
              gloss: entry.gloss,
              category: entry.category,
              durationMs: entry.defaultDurationMs,
              source: 'seed_dictionary',
              animationId: entry.animationId || null
            };
            if (entry.nonManualMarker) {
              signObj.nonManualMarker = entry.nonManualMarker;
            }
            signs.push(signObj);
            i += phraseLen;
            matched = true;
            break;
          }
        }
      }

      if (matched) continue;

      // Check single-word entry
      const token = tokens[i];
      const entry = SINGLE_WORD_LOOKUP.get(token);

      if (entry) {
        const signObj = {
          gloss: entry.gloss,
          category: entry.category,
          durationMs: entry.defaultDurationMs,
          source: 'seed_dictionary',
          animationId: entry.animationId || null
        };
        if (entry.nonManualMarker) {
          signObj.nonManualMarker = entry.nonManualMarker;
        }
        signs.push(signObj);
      } else {
        // Unsupported word tracking
        unsupportedWords.push(token);

        // Optional fingerspelling fallback
        if (options.enableFingerspellingFallback === true) {
          // Decompose token into clean uppercase letters A-Z
          const letters = token.toUpperCase().replace(/[^A-Z]/g, '');
          for (let l = 0; l < letters.length; l++) {
            signs.push({
              gloss: letters[l],
              category: 'fingerspelling',
              durationMs: 300,
              source: 'fingerspell_fallback',
              animationId: null
            });
          }
          if (letters.length > 0) {
            fingerspellingApplied = true;
          }
        }
      }

      i++;
    }

    return { signs, unsupportedWords, fingerspellingApplied };
  }

  // =========================================================================
  // 5. Main Entry Point: translateTranscriptToISL
  // =========================================================================

  /**
   * Main translator function. Transforms raw spoken transcript into a fully
   * validated, immutable SignSequence conforming to Milestone M3 data contracts.
   *
   * @param {string} transcript - Input speech transcript.
   * @param {Object} [options] - Translation options and chunk metadata.
   * @param {string} [options.sequenceId] - Unique sequence ID.
   * @param {number} [options.sourceChunkSeq=0] - Audio sequence chunk counter.
   * @param {number} [options.startMediaTimeMs=0] - Audio media start time in ms.
   * @param {number} [options.endMediaTimeMs] - Audio media end time in ms.
   * @param {boolean} [options.enableExperimentalReordering=false] - Apply experimental grammar heuristic.
   * @param {boolean} [options.enableFingerspellingFallback=false] - Expand unsupported words into A-Z letters.
   * @returns {Readonly<Object>} Validated, immutable SignSequence.
   */
  function translateTranscriptToISL(transcript, options = {}) {
    const rawTranscript = typeof transcript === 'string' ? transcript : '';
    const { normalizedText, tokens, isQuestion } = normalizeTranscript(rawTranscript);

    // Metadata & timing defaults
    const sourceChunkSeq = Number.isInteger(options.sourceChunkSeq) ? options.sourceChunkSeq : 0;
    const startMediaTimeMs = typeof options.startMediaTimeMs === 'number' && Number.isFinite(options.startMediaTimeMs)
      ? Math.max(0, options.startMediaTimeMs)
      : 0;
    const endMediaTimeMs = typeof options.endMediaTimeMs === 'number' && Number.isFinite(options.endMediaTimeMs)
      ? Math.max(startMediaTimeMs, options.endMediaTimeMs)
      : startMediaTimeMs + 2000;

    const sequenceId = typeof options.sequenceId === 'string' && options.sequenceId.trim().length > 0
      ? options.sequenceId.trim()
      : `isl_seq_${sourceChunkSeq}_${Date.now()}`;

    let processingTokens = tokens;

    // Apply isolated experimental grammar heuristics if explicitly enabled
    if (options.enableExperimentalReordering === true) {
      processingTokens = applyExperimentalGrammarHeuristics(tokens, { isQuestion });
    }

    // Match against seed lexicon and extract unsupported words
    const matchResult = matchTokensToSeedLexicon(processingTokens, {
      enableFingerspellingFallback: Boolean(options.enableFingerspellingFallback)
    });

    // Construct and validate complete SignSequence using sign_contracts factory
    const sequence = SignBridgeContracts.createSignSequence({
      sequenceId,
      language: 'ISL',
      rawTranscript,
      sourceChunkSeq,
      startMediaTimeMs,
      endMediaTimeMs,
      signs: matchResult.signs,
      unsupportedWords: matchResult.unsupportedWords,
      fingerspellingApplied: matchResult.fingerspellingApplied
    });

    return sequence;
  }

  // =========================================================================
  // 6. Public Module Exports
  // =========================================================================

  return Object.freeze({
    SEED_LEXICON,
    AUXILIARY_VERBS,
    ARTICLES,
    TEMPORAL_MARKERS,
    QUESTION_WORDS,
    normalizeTranscript,
    applyExperimentalGrammarHeuristics,
    matchTokensToSeedLexicon,
    translateTranscriptToISL
  });
});
