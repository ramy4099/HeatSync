"""FortyGuard / HeatSync Top KPI Cards Component.

Renders real-time metric cards for Ambient Apparent Temp, Recommended Cooling Mode,
PUE Delta, Hourly Cost Savings, and secondary atmospheric indicators.
"""

from typing import Any, Dict
import streamlit as st
from utils.helpers import c_to_f, format_currency, format_co2, get_mode_badge_html


def render_kpi_cards(
    current_metrics: Dict[str, Any],
    kpis: Dict[str, Any],
    facility_meta: Dict[str, Any],
    unit_pref: str = "Celsius (°C)",
    dispatch_rec: Dict[str, Any] = None,
) -> None:
    """Render top operational KPI cards and secondary environmental indicators."""
    is_f = "Fahrenheit" in unit_pref
    temp_unit = "°F" if is_f else "°C"
    
    app_temp_c = float(current_metrics.get("apparent_temperature_celsius", 22.0))
    wet_bulb_c = float(current_metrics.get("wet_bulb_temperature_celsius", 16.5))
    pm25 = float(current_metrics.get("air_quality_pm2p5_idx", 35.0))
    rh = float(current_metrics.get("relative_humidity_percent", 50.0))
    co2_ppm = float(current_metrics.get("co2_ppm", 400.0))
    
    display_temp = c_to_f(app_temp_c) if is_f else app_temp_c
    display_wb = c_to_f(wet_bulb_c) if is_f else wet_bulb_c
    
    rec_mode = current_metrics.get("recommended_mode", "Free-Air Economizer")
    
    projected_pue = float(current_metrics.get("projected_pue", 1.25))
    baseline_pue = float(facility_meta.get("baseline_pue", 1.55))
    pue_delta_pct = float(current_metrics.get("pue_delta_pct", -19.3))
    
    hourly_savings = float(current_metrics.get("hourly_cost_saved_usd", 0.0))
    hourly_kwh_saved = float(current_metrics.get("hourly_kwh_saved", 0.0))

    # 1. Workload Dispatch Banner (if active)
    if dispatch_rec:
        dispatch_html = (
            f'<div style="background: rgba(30, 58, 138, 0.25); border: 1px solid rgba(56, 189, 248, 0.35); border-left: 4px solid #38BDF8; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 1rem;">'
            f'<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">'
            f'<span style="font-size: 0.8rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.04em; display: inline-flex; align-items: center; gap: 6px;">'
            f'<span style="width: 7px; height: 7px; border-radius: 50%; background: #38BDF8;"></span>'
            f'Workload Dispatch Optimization'
            f'</span>'
            f'<span style="background: #0284C7; color: white; padding: 2px 8px; border-radius: 9999px; font-size: 0.7rem; font-weight: 700;">'
            f'Target Facility: {dispatch_rec["target_facility"]}'
            f'</span>'
            f'</div>'
            f'<div style="font-size: 0.82rem; color: #E2E8F0; line-height: 1.4;">'
            f'{dispatch_rec["recommendation"]}'
            f'</div>'
            f'</div>'
        )
        st.markdown(dispatch_html, unsafe_allow_html=True)

    # 2. 4 Primary KPI Columns
    col1, col2, col3, col4 = st.columns(4)

    # Card 1: Ambient Apparent Temperature
    with col1:
        card1_html = (
            f'<div class="kpi-card highlight">'
            f'<div>'
            f'<div class="kpi-title">'
            f'<span>Apparent Temp</span>'
            f'<span style="font-size: 0.68rem; color: #38BDF8; font-weight: 700;">FORTYGUARD</span>'
            f'</div>'
            f'<div class="kpi-value">'
            f'{display_temp:.1f}<span class="kpi-unit">{temp_unit}</span>'
            f'</div>'
            f'</div>'
            f'<div class="kpi-delta delta-neutral">'
            f'<span>Wet-Bulb: {display_wb:.1f}{temp_unit}</span>'
            f'<span style="margin: 0 2px; color: #64748B;">•</span>'
            f'<span>ΔT: {abs(round(app_temp_c - wet_bulb_c, 1))}°C</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card1_html, unsafe_allow_html=True)

    # Card 2: Recommended Cooling Mode
    with col2:
        card_class = "success" if "Free-Air" in rec_mode else ("warning" if "Evaporative" in rec_mode else "danger")
        card2_html = (
            f'<div class="kpi-card {card_class}">'
            f'<div>'
            f'<div class="kpi-title">'
            f'<span>Cooling Dispatch</span>'
            f'<span style="font-size: 0.68rem; color: #94A3B8; font-weight: 700;">ASHRAE TC 9.9</span>'
            f'</div>'
            f'<div style="margin-top: 6px; margin-bottom: 6px;">'
            f'{get_mode_badge_html(rec_mode)}'
            f'</div>'
            f'</div>'
            f'<div style="font-size: 0.75rem; color: #94A3B8; font-weight: 500; margin-top: 4px;">'
            f'{kpis.get("eco_hours", 18)}/24 hrs eco-cooling active'
            f'</div>'
            f'</div>'
        )
        st.markdown(card2_html, unsafe_allow_html=True)

    # Card 3: PUE Efficiency Delta
    with col3:
        pue_delta_class = "delta-positive" if pue_delta_pct < 0 else "delta-neutral"
        pue_val_color = "#10B981" if pue_delta_pct < 0 else "#F8FAFC"
        card3_html = (
            f'<div class="kpi-card highlight">'
            f'<div>'
            f'<div class="kpi-title">'
            f'<span>Facility PUE</span>'
            f'<span style="font-size: 0.68rem; color: #38BDF8; font-weight: 700;">EFFICIENCY</span>'
            f'</div>'
            f'<div class="kpi-value" style="color: {pue_val_color};">'
            f'{projected_pue:.2f}<span class="kpi-unit">Base: {baseline_pue:.2f}</span>'
            f'</div>'
            f'</div>'
            f'<div class="kpi-delta {pue_delta_class}">'
            f'<span>{pue_delta_pct:+.1f}% PUE Shift</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card3_html, unsafe_allow_html=True)

    # Card 4: Estimated Cost Savings
    with col4:
        card4_html = (
            f'<div class="kpi-card success">'
            f'<div>'
            f'<div class="kpi-title">'
            f'<span>Hourly Cost Savings</span>'
            f'<span style="font-size: 0.68rem; color: #10B981; font-weight: 700;">REAL-TIME</span>'
            f'</div>'
            f'<div class="kpi-value" style="color: #10B981;">'
            f'{format_currency(hourly_savings)}<span class="kpi-unit">/hr</span>'
            f'</div>'
            f'</div>'
            f'<div class="kpi-delta delta-positive">'
            f'<span>{hourly_kwh_saved:,.0f} kWh/hr Avoided</span>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card4_html, unsafe_allow_html=True)

    # 3. Secondary Atmospheric & Sustainability Indicators Strip
    pm25_color = '#10B981' if pm25 < 55 else ('#F59E0B' if pm25 < 65 else '#EF4444')
    pm25_label = "Optimal" if pm25 < 55 else ("Moderate" if pm25 < 65 else "Cutoff Filter")
    
    strip_html = (
        f'<div class="env-strip">'
        f'<div class="env-item">'
        f'<div class="env-item-label">Relative Humidity</div>'
        f'<div class="env-item-value">{rh:.0f}%</div>'
        f'</div>'
        f'<div class="env-item">'
        f'<div class="env-item-label">Air Quality (PM2.5)</div>'
        f'<div class="env-item-value" style="color: {pm25_color};">'
        f'{int(pm25)} µg/m³ <span style="font-size: 0.68rem; font-weight: 600; opacity: 0.85;">({pm25_label})</span>'
        f'</div>'
        f'</div>'
        f'<div class="env-item">'
        f'<div class="env-item-label">CO2 Concentration</div>'
        f'<div class="env-item-value">{int(co2_ppm)} ppm</div>'
        f'</div>'
        f'<div class="env-item">'
        f'<div class="env-item-label">24h Projected Savings</div>'
        f'<div class="env-item-value" style="color: #10B981;">'
        f'{format_currency(kpis.get("total_savings_usd", 0.0))}'
        f'</div>'
        f'</div>'
        f'<div class="env-item">'
        f'<div class="env-item-label">Avoided Carbon</div>'
        f'<div class="env-item-value" style="color: #38BDF8;">'
        f'{kpis.get("total_co2_tons", 0.0):.2f} t CO₂e'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(strip_html, unsafe_allow_html=True)


