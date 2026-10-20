/**
 * SignBridge — Milestone M3.5: Sign Language Translation Router
 *
 * Implements centralized language routing between independent sign language pipelines (ISL and ASL).
 *
 * CRITICAL REQUIREMENTS (Requirement 2 & 3):
 * 1. Connect recognized speech transcript events to the selected translation pipeline.
 * 2. Strictly preserve separate ISL and ASL pipelines.
 * 3. Never conflate English word-substitution with sign language translation.
 * 4. Emit validated SignSequence contracts conforming to Milestone M3 data contracts.
 *
 * Architecture Convention:
 * - UMD wrapper compatible with browser extension scripts, Web Workers, and Node.js.
 * - Zero external runtime dependencies.
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    const contracts = require('../models/sign_contracts.js');
    const isl = require('./isl_translator.js');
    const asl = require('./asl_translator.js');
    module.exports = factory(contracts, isl, asl);
  } else if (typeof define === 'function' && define.amd) {
    define(['../models/sign_contracts.js', './isl_translator.js', './asl_translator.js'], factory);
  } else {
    root.SignBridgeTranslationRouter = factory(
      root.SignBridgeContracts || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeContracts : null),
      root.SignBridgeISLTranslator || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeISLTranslator : null),
      root.SignBridgeASLTranslator || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeASLTranslator : null)
    );
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (SignBridgeContracts, SignBridgeISLTranslator, SignBridgeASLTranslator) {
  'use strict';

  if (!SignBridgeContracts) {
    throw new Error('SignBridgeContracts dependency is required by TranslationRouter.');
  }

  const SUPPORTED_LANGUAGES = Object.freeze(['ISL', 'ASL']);
  const DEFAULT_LANGUAGE = 'ISL';

  class TranslationRouterError extends Error {
    constructor(message, code = 'ROUTING_ERROR') {
      super(message);
      this.name = 'TranslationRouterError';
      this.code = code;
    }
  }

  /**
   * Routes a recognized spoken transcript to the specified sign language translator.
   *
   * @param {string} transcript - Input speech transcript text.
   * @param {string} [targetLanguage='ISL'] - Target sign language ('ISL' or 'ASL').
   * @param {Object} [options] - Translation options and chunk metadata.
   * @returns {Readonly<Object>} Validated SignSequence.
   */
  function routeTranscriptTranslation(transcript, targetLanguage = DEFAULT_LANGUAGE, options = {}) {
    const rawTranscript = typeof transcript === 'string' ? transcript : '';
    const lang = (typeof targetLanguage === 'string' ? targetLanguage.trim().toUpperCase() : DEFAULT_LANGUAGE);

    if (!SUPPORTED_LANGUAGES.includes(lang)) {
      throw new TranslationRouterError(
        `Unsupported target sign language '${targetLanguage}'. Must be one of: [${SUPPORTED_LANGUAGES.join(', ')}]`,
        'UNSUPPORTED_LANGUAGE'
      );
    }

    if (lang === 'ISL') {
      if (!SignBridgeISLTranslator || typeof SignBridgeISLTranslator.translateTranscriptToISL !== 'function') {
        throw new TranslationRouterError('SignBridgeISLTranslator is not loaded.', 'TRANSLATOR_UNAVAILABLE');
      }
      return SignBridgeISLTranslator.translateTranscriptToISL(rawTranscript, options);
    }

    if (lang === 'ASL') {
      if (!SignBridgeASLTranslator || typeof SignBridgeASLTranslator.translateTranscriptToASL !== 'function') {
        throw new TranslationRouterError('SignBridgeASLTranslator is not loaded.', 'TRANSLATOR_UNAVAILABLE');
      }
      return SignBridgeASLTranslator.translateTranscriptToASL(rawTranscript, options);
    }

    throw new TranslationRouterError(`Routing unhandled for language '${lang}'`, 'UNHANDLED_ROUTING');
  }

  return Object.freeze({
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    TranslationRouterError,
    routeTranscriptTranslation,
    isLanguageSupported: (lang) => typeof lang === 'string' && SUPPORTED_LANGUAGES.includes(lang.trim().toUpperCase())
  });
});
