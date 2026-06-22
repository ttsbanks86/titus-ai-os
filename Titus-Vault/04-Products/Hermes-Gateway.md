# Hermes Gateway

## Overview
An API gateway and model router that provides a unified interface for accessing multiple AI models. Routes requests to the best available model based on task type, cost, and availability.

## Current State
- Phase: In Use / Active
- Last updated: 2026-06-21
- Status: Hermes runs via OpenRouter with deepseek-v4-flash
- Config: `C:\Users\tbank\AppData\Local\hermes\config.yaml`

## Goals
- Provide reliable model routing for Hermes
- Support fallback chains when primary models are unavailable
- Maintain cost-effective model selection

## Linked Notes
- [[08-Agents/Hermes-Agent]]
- [[09-Knowledge/AI-Systems/Model-Routing]]
- [[09-Knowledge/AI-Systems/Provider-Architecture]]
- [[04-Products/Products]]

## Active Tasks
- [ ] Review Hermes config for optimal routing
- [ ] Ensure fallback chains are configured

## Decisions Made
- 2026-06-21: Hermes updated to vault-based context — reads Home.md instead of scanning all files
