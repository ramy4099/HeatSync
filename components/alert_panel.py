"""FortyGuard / HeatSync AI Operational Narrative & Alert Component.

Renders generative operational briefings (LangChain / Gemini) and
rule-based forecast alert triggers (Critical Chiller Peaks, Air Quality cutoffs).
"""

import re
from typing import Any, Dict, List
import streamlit as st
from utils.helpers import SEVERITY_MAP


def format_markdown_to_html(text: str) -> str:
    """Helper to convert basic markdown (bold, italic, lists) into clean HTML."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #F8FAFC;">\1</strong>', text)
    text = text.replace('\n\n', '<div style="margin-top: 0.45rem;"></div>').replace('\n', '<br>')
    return text


def render_alert_panel(narrative_text: str, alerts: List[Dict[str, Any]], facility_name: str) -> None:
    """Render the AI Operational Narrative and Actionable Alerts Panel in an executive 2-column layout."""
    formatted_narrative = format_markdown_to_html(narrative_text)

    col_briefing, col_alerts = st.columns([1.3, 1.0])

    with col_briefing:
        briefing_html = (
            f'<div class="kpi-card highlight" style="padding: 1.25rem; height: 100%;">'
            f'<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; border-bottom: 1px solid #1E293B; padding-bottom: 0.5rem;">'
            f'<div style="display: flex; align-items: center; gap: 8px;">'
            f'<span style="width: 8px; height: 8px; border-radius: 50%; background: #38BDF8; display: inline-block;"></span>'
            f'<span style="font-size: 0.88rem; font-weight: 700; color: #F8FAFC;">Operational Intelligence Briefing</span>'
            f'</div>'
            f'<span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.04em;">'
            f'Gemini AI / LangGraph'
            f'</span>'
            f'</div>'
            f'<div style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.65;">'
            f'{formatted_narrative}'
            f'</div>'
            f'</div>'
        )
        st.markdown(briefing_html, unsafe_allow_html=True)

    with col_alerts:
        alert_count = len(alerts)
        badge_bg = "rgba(239, 68, 68, 0.15)" if alert_count > 0 else "rgba(16, 185, 129, 0.15)"
        badge_border = "rgba(239, 68, 68, 0.35)" if alert_count > 0 else "rgba(16, 185, 129, 0.3)"
        badge_color = "#EF4444" if alert_count > 0 else "#10B981"
        badge_label = f"{alert_count} Active" if alert_count > 0 else "Nominal"

        alerts_container_header = (
            f'<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">'
            f'<span style="font-size: 0.84rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.04em;">'
            f'Forecast Safeguards & Alerts'
            f'</span>'
            f'<span style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.68rem; font-weight: 700;">'
            f'{badge_label}'
            f'</span>'
            f'</div>'
        )
        st.markdown(alerts_container_header, unsafe_allow_html=True)

        if alerts:
            for alt in alerts:
                sev_key = alt.get("severity", "info").lower()
                sev_cfg = SEVERITY_MAP.get(sev_key, SEVERITY_MAP["info"])
                alt_html = (
                    f'<div class="alert-item {sev_cfg["class"]}" style="margin-bottom: 0.5rem;">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">'
                    f'<span style="font-weight: 700; font-size: 0.82rem; color: #F8FAFC;">{alt["title"]}</span>'
                    f'<div style="display: flex; align-items: center; gap: 6px;">'
                    f'<span style="font-size: 0.7rem; color: #94A3B8;">{alt.get("timestamp", "")}</span>'
                    f'<span style="background: {sev_cfg["color"]}; color: white; padding: 1px 6px; border-radius: 3px; font-size: 0.64rem; font-weight: 700;">'
                    f'{sev_cfg["badge"]}'
                    f'</span>'
                    f'</div>'
                    f'</div>'
                    f'<div style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.45;">'
                    f'{alt["message"]}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(alt_html, unsafe_allow_html=True)
        else:
            empty_html = (
                f'<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 0.85rem 1rem; font-size: 0.8rem; color: #10B981; line-height: 1.5;">'
                f'<div style="font-weight: 700; margin-bottom: 2px;">✓ Zero Active Alerts</div>'
                f'<div style="color: #94A3B8; font-size: 0.76rem;">No critical thermal spikes or particulate threshold exceedances projected in the next 12 hours.</div>'
                f'</div>'
            )
            st.markdown(empty_html, unsafe_allow_html=True)


