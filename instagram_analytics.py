from html import escape

import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Instagram Insights",
    page_icon="📸",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff5f9 0%, #ffffff 55%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 5% 0%, rgba(255, 214, 231, 0.9), transparent 30%),
            linear-gradient(180deg, #fff8fb 0%, #fff1f6 100%);
        border-right: 1px solid #f3dbe6;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding: 1.1rem 1rem 2rem;
    }

    .sidebar-brand {
        margin: 0.5rem 0 1.3rem;
        padding: 1.15rem;
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        color: #ffffff;
        background:
            radial-gradient(circle at 100% 0%, rgba(255, 255, 255, 0.2), transparent 38%),
            linear-gradient(145deg, #651b4b 0%, #bd3475 62%, #ed658d 100%);
        box-shadow: 0 12px 28px rgba(183, 41, 106, 0.18);
    }

    .sidebar-brand-top {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }

    .sidebar-brand .logo-mark {
        width: 40px;
        height: 40px;
        flex-basis: 40px;
        border-radius: 13px;
    }

    .sidebar-brand .logo-camera {
        transform: scale(0.82);
    }

    .sidebar-wordmark {
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.14em;
    }

    .sidebar-wordmark span {
        display: block;
        margin-top: 0.18rem;
        color: #ffdce9;
        font-size: 0.62rem;
        letter-spacing: 0.2em;
    }

    .sidebar-kicker {
        margin-top: 1.15rem;
        color: #ffdce9;
        font-size: 0.63rem;
        font-weight: 800;
        letter-spacing: 0.15em;
    }

    .sidebar-brand h2 {
        margin: 0.35rem 0 0.3rem;
        color: #ffffff;
        font-size: 1.25rem;
        letter-spacing: -0.035em;
    }

    .sidebar-brand p {
        margin: 0;
        color: #ffeaf1;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .sidebar-section-label {
        margin: 1.1rem 0 0.3rem;
        color: #a26d87;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .sidebar-summary {
        margin-top: 1rem;
        padding: 1rem;
        border: 1px solid #f2dce7;
        border-radius: 17px;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 22px rgba(117, 41, 79, 0.05);
    }

    .sidebar-summary-label {
        color: #98778a;
        font-size: 0.66rem;
        font-weight: 750;
        letter-spacing: 0.12em;
    }

    .sidebar-summary-value {
        margin: 0.2rem 0;
        color: #a42662;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .sidebar-summary-note {
        color: #746473;
        font-size: 0.78rem;
    }

    [data-testid="stSidebar"] .stButton > button {
        min-height: 2.8rem;
        border: 1px solid #f1d3e1;
        border-radius: 12px;
        color: #a42662;
        background: rgba(255, 255, 255, 0.78);
        font-weight: 700;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #e7a9c2;
        color: #8e1c54;
        background: #ffffff;
        box-shadow: 0 7px 18px rgba(183, 41, 106, 0.1);
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] {
        padding: 0.55rem 0.7rem 0.7rem;
        border: 1px solid #f1dce6;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.78);
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] label {
        color: #654357;
        font-size: 0.83rem;
        font-weight: 650;
    }

    .hero {
        position: relative;
        overflow: hidden;
        display: grid;
        grid-template-columns: minmax(0, 1.05fr) minmax(300px, 0.95fr);
        align-items: center;
        gap: clamp(2rem, 5vw, 5rem);
        min-height: 490px;
        padding: clamp(2rem, 5vw, 4.5rem);
        border: 1px solid #eadbd0;
        border-radius: 30px;
        color: #34251f;
        background:
            radial-gradient(circle at 0% 100%, rgba(231, 195, 164, 0.24), transparent 34%),
            linear-gradient(135deg, #fffdf9 0%, #faf4ed 100%);
        box-shadow: 0 24px 70px rgba(83, 54, 37, 0.09);
    }

    .hero-brand,
    .dashboard-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .hero-brand {
        margin-bottom: 2.8rem;
    }

    .hero-brand .brand-name {
        color: #4a2d24;
    }

    .hero-brand .brand-subtitle {
        color: #9a6d55;
    }

    .logo-mark {
        display: grid;
        width: 48px;
        height: 48px;
        flex: 0 0 48px;
        place-items: center;
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 15px;
        background: linear-gradient(140deg, #feda75 0%, #fa7e1e 28%, #d62976 58%, #962fbf 82%, #4f5bd5 100%);
        box-shadow: 0 8px 22px rgba(39, 13, 49, 0.2);
    }

    .logo-camera {
        position: relative;
        display: block;
        width: 23px;
        height: 23px;
        border: 2px solid #ffffff;
        border-radius: 7px;
    }

    .logo-lens {
        position: absolute;
        top: 5px;
        left: 5px;
        width: 9px;
        height: 9px;
        border: 2px solid #ffffff;
        border-radius: 50%;
    }

    .logo-flash {
        position: absolute;
        top: 3px;
        right: 3px;
        width: 3px;
        height: 3px;
        border-radius: 50%;
        background: #ffffff;
    }

    .brand-name {
        display: block;
        color: #ffffff;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.16em;
    }

    .brand-subtitle {
        display: block;
        margin-top: 0.18rem;
        color: #f9dce8;
        font-size: 0.68rem;
        font-weight: 650;
        letter-spacing: 0.2em;
    }

    .dashboard-banner {
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
        padding: clamp(1.5rem, 4vw, 2.6rem);
        border-radius: 26px;
        color: white;
        background:
            radial-gradient(circle at 92% 10%, rgba(255, 255, 255, 0.24), transparent 24%),
            linear-gradient(120deg, #5a1746 0%, #bd2f75 58%, #f06a91 100%);
        box-shadow: 0 18px 48px rgba(183, 41, 106, 0.18);
    }

    .dashboard-banner h1 {
        margin: 1.6rem 0 0.45rem;
        color: #ffffff;
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 760;
        letter-spacing: -0.045em;
    }

    .dashboard-banner p {
        margin: 0;
        color: #ffe8f0;
        font-size: 1rem;
    }

    .live-pill {
        margin-left: auto;
        padding: 0.5rem 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 999px;
        color: #fff3f7;
        background: rgba(255, 255, 255, 0.12);
        font-size: 0.7rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        white-space: nowrap;
    }

    .live-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: 0.45rem;
        border-radius: 50%;
        background: #ffd166;
        box-shadow: 0 0 0 4px rgba(255, 209, 102, 0.18);
        vertical-align: 1px;
    }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 1rem;
        color: #9a5c3c;
        font-size: 0.69rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .hero-eyebrow::before {
        width: 22px;
        height: 1px;
        background: #c47a50;
        content: "";
    }

    .hero h1 {
        max-width: 620px;
        margin: 0;
        color: #34251f;
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(2.65rem, 5.2vw, 4.65rem);
        font-weight: 500;
        letter-spacing: -0.06em;
        line-height: 0.99;
    }

    .hero h1 span {
        color: #bb6945;
        font-style: italic;
        font-weight: 500;
    }

    .hero-copy {
        max-width: 650px;
        margin: 1.25rem 0 0;
        color: #76665d;
        font-size: clamp(0.98rem, 1.4vw, 1.08rem);
        line-height: 1.75;
    }

    .hero-note {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-top: 1.6rem;
        color: #8c7567;
        font-size: 0.76rem;
        font-weight: 650;
        letter-spacing: 0.03em;
    }

    .hero-note-mark {
        display: grid;
        width: 25px;
        height: 25px;
        place-items: center;
        border: 1px solid #e6d3c5;
        border-radius: 50%;
        color: #a7603f;
        background: #fffaf4;
        font-size: 0.72rem;
    }

    .hero-copy-column .hero-brand,
    .hero-eyebrow,
    .hero h1,
    .hero-copy,
    .hero-note {
        animation: intro-copy-enter 680ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    .hero-copy-column .hero-brand {
        animation-delay: 80ms;
    }

    .hero-eyebrow {
        animation-delay: 180ms;
    }

    .hero h1 {
        animation-delay: 280ms;
    }

    .hero-copy {
        animation-delay: 390ms;
    }

    .hero-note {
        animation-delay: 500ms;
    }

    .hero-visual {
        position: relative;
        display: grid;
        min-height: 330px;
        place-items: center;
        isolation: isolate;
        animation: intro-visual-enter 950ms cubic-bezier(0.2, 0.75, 0.25, 1) 180ms both;
    }

    .hero-orbit {
        position: absolute;
        z-index: -1;
        width: min(94%, 390px);
        aspect-ratio: 1;
        border: 1px solid rgba(188, 132, 99, 0.2);
        border-radius: 50%;
        background:
            radial-gradient(circle at 50% 50%, rgba(231, 195, 164, 0.32), transparent 66%),
            repeating-radial-gradient(circle at 50% 50%, transparent 0 53px, rgba(188, 132, 99, 0.1) 54px 55px);
        animation: intro-orbit-turn 38s linear 1.1s infinite;
    }

    .insight-preview {
        position: relative;
        width: min(100%, 350px);
        padding: 1.35rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 23px;
        color: #fff8f1;
        background:
            radial-gradient(circle at 100% 0%, rgba(216, 145, 105, 0.22), transparent 38%),
            linear-gradient(145deg, #392922 0%, #241b19 100%);
        box-shadow: 0 26px 55px rgba(62, 39, 28, 0.24);
        transform: rotate(-2deg);
        transition: transform 320ms cubic-bezier(0.2, 0.75, 0.25, 1), box-shadow 320ms ease;
    }

    .hero-visual:hover .insight-preview {
        transform: rotate(0deg) translateY(-4px);
        box-shadow: 0 32px 64px rgba(62, 39, 28, 0.3);
    }

    .preview-topline,
    .preview-metric-row,
    .preview-chart-heading,
    .preview-label-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .preview-topline {
        color: #d7c3b4;
        font-size: 0.62rem;
        font-weight: 750;
        letter-spacing: 0.15em;
    }

    .preview-pill {
        padding: 0.32rem 0.5rem;
        border: 1px solid rgba(255, 225, 203, 0.22);
        border-radius: 999px;
        color: #f0c4a6;
        font-size: 0.56rem;
        letter-spacing: 0.1em;
    }

    .preview-metric-row {
        align-items: flex-end;
        margin-top: 1.5rem;
    }

    .preview-label {
        color: #c8b3a5;
        font-size: 0.74rem;
    }

    .preview-value {
        margin-top: 0.25rem;
        color: #fffaf5;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2.3rem;
        letter-spacing: -0.055em;
        line-height: 1;
    }

    .preview-change {
        padding: 0.4rem 0.55rem;
        border-radius: 9px;
        color: #bee0b5;
        background: rgba(149, 194, 131, 0.12);
        font-size: 0.68rem;
        font-weight: 750;
    }

    .preview-chart {
        display: flex;
        height: 112px;
        align-items: flex-end;
        gap: 0.55rem;
        margin-top: 1.25rem;
        padding: 0.85rem 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.035);
    }

    .preview-bar {
        flex: 1;
        min-height: 14px;
        border-radius: 6px 6px 2px 2px;
        background: linear-gradient(180deg, #eab28c 0%, #a96145 100%);
        opacity: 0.88;
        transform: scaleY(0.08);
        transform-origin: bottom;
        animation: intro-bar-rise 620ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    .preview-bar:nth-child(1) { animation-delay: 520ms; }
    .preview-bar:nth-child(2) { animation-delay: 590ms; }
    .preview-bar:nth-child(3) { animation-delay: 660ms; }
    .preview-bar:nth-child(4) { animation-delay: 730ms; }
    .preview-bar:nth-child(5) { animation-delay: 800ms; }
    .preview-bar:nth-child(6) { animation-delay: 870ms; }
    .preview-bar:nth-child(7) { animation-delay: 940ms; }

    .preview-float {
        animation: intro-float-enter 760ms cubic-bezier(0.2, 0.75, 0.25, 1) 720ms both;
    }

    .preview-bar:nth-child(2n) {
        background: linear-gradient(180deg, #f3d4b8 0%, #bf7958 100%);
        opacity: 0.72;
    }

    .preview-label-row {
        margin-top: 0.6rem;
        color: #a99283;
        font-size: 0.58rem;
    }

    .preview-float {
        position: absolute;
        right: -0.45rem;
        bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.8rem 1rem;
        border: 1px solid #efe3d8;
        border-radius: 15px;
        color: #48362c;
        background: #fffdf9;
        box-shadow: 0 14px 32px rgba(62, 39, 28, 0.14);
        transform: rotate(3deg);
    }

    .preview-float-icon {
        display: grid;
        width: 34px;
        height: 34px;
        place-items: center;
        border-radius: 11px;
        color: #a85e3d;
        background: #f8ece2;
        font-size: 1rem;
    }

    .preview-float-label {
        color: #947a6b;
        font-size: 0.57rem;
        font-weight: 750;
        letter-spacing: 0.1em;
    }

    .preview-float-value {
        margin-top: 0.15rem;
        font-size: 0.8rem;
        font-weight: 800;
    }

    .feature-card {
        height: 100%;
        min-height: 178px;
        padding: 1.4rem;
        border: 1px solid #ebded3;
        border-radius: 18px;
        background: rgba(255, 253, 249, 0.88);
        box-shadow: 0 12px 34px rgba(83, 54, 37, 0.045);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .feature-card:hover {
        transform: translateY(-5px) rotate(-0.4deg);
        border-color: #d9b59f;
        box-shadow: 0 18px 38px rgba(83, 54, 37, 0.1);
    }

    .intro-section-heading {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin: 2.1rem 0 1rem;
    }

    .intro-section-kicker {
        color: #a66a4d;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .intro-section-heading h2 {
        margin: 0.28rem 0 0;
        color: #3d2c24;
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(1.45rem, 2.2vw, 1.85rem);
        font-weight: 500;
        letter-spacing: -0.04em;
    }

    .intro-section-note {
        margin: 0 0 0.2rem;
        color: #907b6e;
        font-size: 0.78rem;
    }

    .feature-icon {
        display: grid;
        width: 42px;
        height: 42px;
        place-items: center;
        margin-bottom: 0.7rem;
        border: 1px solid #ead7c8;
        border-radius: 14px;
        color: #a85e3d;
        background: #f8eee5;
        font-size: 1.2rem;
        transition: transform 220ms cubic-bezier(0.2, 0.75, 0.25, 1), background-color 220ms ease;
    }

    .feature-card:hover .feature-icon {
        transform: rotate(-8deg) scale(1.08);
        background: #f3e2d4;
    }

    .feature-card h3 {
        margin: 0 0 0.4rem;
        color: #3d2c24;
        font-size: 1.08rem;
    }

    .feature-card p {
        margin: 0;
        color: #806f64;
        font-size: 0.93rem;
        line-height: 1.55;
    }

    [data-testid="stMetric"] {
        position: relative;
        min-height: 112px;
        padding: 1.2rem 1.25rem;
        border: 1px solid #f1dfe8;
        border-radius: 20px;
        background:
            radial-gradient(circle at 100% 0%, rgba(255, 215, 232, 0.5), transparent 42%),
            linear-gradient(145deg, #ffffff 0%, #fffafd 100%);
        box-shadow: 0 10px 28px rgba(117, 41, 79, 0.06);
        transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
        animation: metric-enter 520ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    [data-testid="stMetric"]::before {
        position: absolute;
        top: 0;
        left: 1.25rem;
        width: 42px;
        height: 3px;
        border-radius: 0 0 999px 999px;
        background: linear-gradient(90deg, #f8a5c2, #d63378);
        content: "";
        transition: width 220ms ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #eab3cb;
        box-shadow: 0 18px 34px rgba(183, 41, 106, 0.13);
    }

    [data-testid="stMetric"]:hover::before {
        width: calc(100% - 2.5rem);
    }

    [data-testid="stMetricLabel"] {
        color: #806b7a;
        font-size: 0.82rem;
        font-weight: 650;
    }

    [data-testid="stMetricValue"] {
        color: #a42662;
        font-size: clamp(1.7rem, 2.5vw, 2.25rem);
        font-weight: 780;
        letter-spacing: -0.045em;
    }

    .dashboard-section-heading {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin: 0.4rem 0 1rem;
    }

    .dashboard-section-kicker {
        color: #b04a78;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .dashboard-section-heading h2 {
        margin: 0.25rem 0 0;
        color: #46283a;
        font-size: clamp(1.25rem, 2vw, 1.6rem);
        letter-spacing: -0.035em;
    }

    .dashboard-section-heading p {
        margin: 0.3rem 0 0;
        color: #806b7a;
        font-size: 0.9rem;
    }

    .dashboard-section-badge {
        padding: 0.45rem 0.7rem;
        border: 1px solid #f1d4e2;
        border-radius: 999px;
        color: #a42662;
        background: rgba(255, 255, 255, 0.8);
        font-size: 0.7rem;
        font-weight: 750;
        white-space: nowrap;
    }

    @keyframes metric-enter {
        from {
            opacity: 0;
            transform: translateY(10px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes intro-copy-enter {
        from {
            opacity: 0;
            transform: translateY(18px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes intro-visual-enter {
        from {
            opacity: 0;
            transform: translateX(24px) scale(0.96);
        }

        to {
            opacity: 1;
            transform: translateX(0) scale(1);
        }
    }

    @keyframes intro-bar-rise {
        from {
            transform: scaleY(0.08);
            filter: brightness(1.35);
        }

        to {
            transform: scaleY(1);
            filter: brightness(1);
        }
    }

    @keyframes intro-float-enter {
        from {
            opacity: 0;
            transform: translateY(12px) rotate(3deg);
        }

        to {
            opacity: 1;
            transform: translateY(0) rotate(3deg);
        }
    }

    @keyframes intro-orbit-turn {
        to {
            transform: rotate(360deg);
        }
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #f0dce6;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.78);
        box-shadow: 0 10px 28px rgba(117, 41, 79, 0.045);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 15px 34px rgba(183, 41, 106, 0.1);
    }

    .st-key-chart-media,
    .st-key-chart-category,
    .st-key-chart-hour {
        position: relative;
        overflow: hidden;
        margin: 0.8rem 0 1.25rem;
        padding: 0.7rem 1rem 0.35rem;
        border: 1px solid #f1d4e2;
        border-radius: 22px;
        background:
            radial-gradient(ellipse at 100% 0%, rgba(255, 215, 232, 0.62), transparent 38%),
            linear-gradient(145deg, #ffffff 0%, #fff8fb 54%, #fff0f6 100%);
        box-shadow:
            0 14px 36px rgba(143, 45, 93, 0.07),
            inset 0 1px 0 rgba(255, 255, 255, 0.95);
        transition:
            transform 240ms cubic-bezier(0.2, 0.75, 0.25, 1),
            box-shadow 240ms ease,
            border-color 240ms ease;
    }

    .st-key-chart-media::before,
    .st-key-chart-category::before,
    .st-key-chart-hour::before {
        position: absolute;
        top: 0;
        right: 12%;
        left: 12%;
        height: 3px;
        border-radius: 0 0 999px 999px;
        background: linear-gradient(90deg, #f8a5c2, #d63378, #8e44ad);
        content: "";
        opacity: 0.8;
    }

    .st-key-chart-media:hover,
    .st-key-chart-category:hover,
    .st-key-chart-hour:hover {
        transform: translateY(-4px);
        border-color: #eab3cb;
        box-shadow:
            0 22px 44px rgba(143, 45, 93, 0.13),
            inset 0 1px 0 rgba(255, 255, 255, 0.95);
    }

    .st-key-chart-media,
    .st-key-chart-category {
        min-height: 425px;
    }

    .st-key-chart-hour {
        min-height: 430px;
    }

    .st-key-chart-media h3,
    .st-key-chart-category h3,
    .st-key-chart-hour h3 {
        color: #572c45;
        font-size: 1.15rem;
        letter-spacing: -0.02em;
    }

    [data-testid="stPlotlyChart"] {
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.48);
    }

    .st-key-data-library {
        margin-top: 1.5rem;
        padding: 1.25rem;
        border: 1px solid #f1d4e2;
        border-radius: 22px;
        background:
            radial-gradient(ellipse at 100% 0%, rgba(255, 215, 232, 0.42), transparent 40%),
            linear-gradient(145deg, #ffffff 0%, #fff8fb 100%);
        box-shadow: 0 14px 36px rgba(143, 45, 93, 0.07);
        transition: box-shadow 220ms ease, border-color 220ms ease;
    }

    .st-key-data-library:hover {
        border-color: #eab3cb;
        box-shadow: 0 18px 40px rgba(143, 45, 93, 0.11);
    }

    .data-library-heading {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        margin: 0.1rem 0 0.9rem;
    }

    .data-library-kicker {
        color: #b04a78;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .data-library-heading h2 {
        margin: 0.25rem 0 0;
        color: #46283a;
        font-size: 1.35rem;
        letter-spacing: -0.035em;
    }

    .data-library-heading p {
        margin: 0.35rem 0 0;
        color: #806b7a;
        font-size: 0.88rem;
    }

    .data-library-count {
        padding: 0.45rem 0.7rem;
        border: 1px solid #f1d4e2;
        border-radius: 999px;
        color: #a42662;
        background: rgba(255, 255, 255, 0.82);
        font-size: 0.7rem;
        font-weight: 750;
        white-space: nowrap;
    }

    .st-key-data-library [data-testid="stExpander"] details {
        overflow: hidden;
        border: 1px solid #efd6e2;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.82);
        transition: border-color 180ms ease, box-shadow 180ms ease;
    }

    .st-key-data-library [data-testid="stExpander"] details:hover,
    .st-key-data-library [data-testid="stExpander"] details[open] {
        border-color: #e5a9c2;
        box-shadow: 0 8px 22px rgba(183, 41, 106, 0.08);
    }

    .st-key-data-library [data-testid="stExpander"] summary {
        min-height: 3.2rem;
        color: #76284f;
        font-weight: 700;
        transition: background-color 180ms ease;
    }

    .st-key-data-library [data-testid="stExpander"] summary:hover {
        background: #fff3f8;
    }

    .st-key-data-library [data-testid="stExpander"] [data-testid="stDataFrame"] {
        border: 1px solid #f1e2e9;
        border-radius: 12px;
        overflow: hidden;
    }

    .motion-ready {
        opacity: 0;
        transform: translateY(14px);
        transition: opacity 480ms ease, transform 480ms cubic-bezier(0.2, 0.75, 0.25, 1);
    }

    .motion-ready.motion-visible {
        opacity: 1;
        transform: translateY(0);
    }

    .stButton > button {
        min-height: 3rem;
        border: 0;
        border-radius: 12px;
        font-weight: 650;
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    .stButton > button[kind="primary"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #d52d73, #f0648b) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(213, 45, 115, 0.2);
    }

    @media (max-width: 640px) {
        .hero {
            grid-template-columns: 1fr;
            gap: 1.2rem;
            min-height: auto;
            border-radius: 22px;
        }

        .hero-brand {
            margin-bottom: 2rem;
        }

        .hero-visual {
            min-height: 290px;
        }

        .insight-preview {
            width: min(92%, 350px);
        }

        .preview-float {
            right: 0;
        }

        .intro-section-heading {
            align-items: flex-start;
            flex-direction: column;
        }

        .live-pill {
            display: none;
        }

        .dashboard-section-heading {
            align-items: flex-start;
            flex-direction: column;
        }

        .st-key-chart-media,
        .st-key-chart-category,
        .st-key-chart-hour {
            min-height: auto;
            padding-right: 0.5rem;
            padding-left: 0.5rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
            animation-duration: 0.01ms !important;
        }

        .hero-copy-column .hero-brand,
        .hero-eyebrow,
        .hero h1,
        .hero-copy,
        .hero-note,
        .hero-visual,
        .hero-orbit,
        .preview-bar,
        .preview-float {
            opacity: 1;
            transform: none;
            animation: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.html(
    """
    <script>
    (() => {
        if (window.__instagramInsightsObserver) {
            window.__instagramInsightsObserver.disconnect();
        }

        const revealContent = () => {
            if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
            document.querySelectorAll(
                ".hero, .dashboard-banner, .feature-card, [data-testid='stMetric'], " +
                ".st-key-chart-media, .st-key-chart-category, .st-key-chart-hour"
            ).forEach((element, index) => {
                if (element.dataset.revealReady) return;
                element.dataset.revealReady = "true";
                element.classList.add("motion-ready");
                element.style.transitionDelay = `${Math.min(index * 70, 350)}ms`;
                requestAnimationFrame(() => element.classList.add("motion-visible"));
            });
        };

        revealContent();
        const observer = new MutationObserver(revealContent);
        window.__instagramInsightsObserver = observer;
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        setTimeout(() => observer.disconnect(), 30000);
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)

instagram_logo = """
<span class="logo-mark" aria-label="Instagram logo">
    <span class="logo-camera" aria-hidden="true">
        <span class="logo-lens"></span>
        <span class="logo-flash"></span>
    </span>
</span>
"""

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    st.html(
        f"""
        <section class="hero">
            <div class="hero-copy-column">
                <div class="hero-brand">
                    {instagram_logo}
                    <div>
                        <span class="brand-name">INSTAGRAM</span>
                        <span class="brand-subtitle">INSIGHTS STUDIO</span>
                    </div>
                </div>
                <div class="hero-eyebrow">A field guide for your content</div>
                <h1>Read the story<br>behind every <span>post.</span></h1>
                <p class="hero-copy">
                    Go beyond the scroll. See what earns attention, which formats
                    connect, and when your audience is ready to engage.
                </p>
                <div class="hero-note">
                    <span class="hero-note-mark">↗</span>
                    Clear signals. More confident next moves.
                </div>
            </div>
            <div class="hero-visual" aria-label="Illustration of the analytics dashboard">
                <div class="hero-orbit" aria-hidden="true"></div>
                <div class="insight-preview">
                    <div class="preview-topline">
                        <span>CONTENT PULSE</span>
                        <span class="preview-pill">SAMPLE VIEW</span>
                    </div>
                    <div class="preview-metric-row">
                        <div>
                            <div class="preview-label">Engagement trend</div>
                            <div class="preview-value">+18.6%</div>
                        </div>
                        <span class="preview-change">↗ this week</span>
                    </div>
                    <div class="preview-chart" aria-hidden="true">
                        <span class="preview-bar" style="height: 34%"></span>
                        <span class="preview-bar" style="height: 52%"></span>
                        <span class="preview-bar" style="height: 43%"></span>
                        <span class="preview-bar" style="height: 70%"></span>
                        <span class="preview-bar" style="height: 57%"></span>
                        <span class="preview-bar" style="height: 86%"></span>
                        <span class="preview-bar" style="height: 100%"></span>
                    </div>
                    <div class="preview-label-row">
                        <span>MON</span><span>TUE</span><span>WED</span><span>THU</span>
                        <span>FRI</span><span>SAT</span><span>SUN</span>
                    </div>
                </div>
                <div class="preview-float">
                    <span class="preview-float-icon">◷</span>
                    <span>
                        <span class="preview-float-label">AUDIENCE WINDOW</span>
                        <span class="preview-float-value">Find your best time</span>
                    </span>
                </div>
            </div>
        </section>
        """
    )

    st.html(
        """
        <div class="intro-section-heading">
            <div>
                <div class="intro-section-kicker">From numbers to next moves</div>
                <h2>Three ways to know your content better.</h2>
            </div>
            <p class="intro-section-note">A little clarity goes a long way.</p>
        </div>
        """
    )
    feature_columns = st.columns(3)
    features = [
        ("✳", "Read the response", "Bring likes, comments, shares, and saves into one clearer picture."),
        ("▤", "Find your format", "Compare media types and categories to see what resonates."),
        ("◷", "Choose your moment", "Explore when your audience is most active and engaged."),
    ]
    for column, (icon, title, description) in zip(feature_columns, features):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    _, action_column, _ = st.columns([1, 1.2, 1])
    with action_column:
        if st.button("Open your insights  →", type="primary", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()

    st.stop()

# Connect to MySQL
@st.cache_data(ttl=300)
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="blessyouharman8102004",
        database="instagram_analytics"
    )

    df = pd.read_sql("SELECT * FROM instagram_posts", conn)
    conn.close()
    return df

df = load_data()

with st.sidebar:
    st.html(
        f"""
        <div class="sidebar-brand">
            <div class="sidebar-brand-top">
                {instagram_logo}
                <div class="sidebar-wordmark">
                    INSTAGRAM
                    <span>INSIGHTS STUDIO</span>
                </div>
            </div>
            <div class="sidebar-kicker">CREATOR ANALYTICS</div>
            <h2>Make your next move.</h2>
            <p>A clearer view of what your audience loves.</p>
        </div>
        """
    )

if st.sidebar.button("← Introduction", use_container_width=True):
    st.session_state.show_dashboard = False
    st.rerun()

# Calculate engagement
df["total_engagement"] = (
    df["likes"] + df["comments"] +
    df["shares"] + df["saves"]
)

# Dashboard title
st.html(
    f"""
    <section class="dashboard-banner">
        <div class="dashboard-brand">
            {instagram_logo}
            <span class="live-pill"><span class="live-dot"></span>YOUR INSIGHTS</span>
        </div>
        <h1>Your content, decoded.</h1>
        <p>Social performance at a glance. Find the signal behind every post.</p>
    </section>
    """
)

# Sidebar filters
st.sidebar.markdown(
    '<div class="sidebar-section-label">Refine your view</div>',
    unsafe_allow_html=True,
)
st.sidebar.subheader("Content filters")

media_options = ["All"] + sorted(df["media_type"].dropna().unique().tolist())

selected_media = st.sidebar.selectbox(
    "Select Media Type",
    media_options
)

filtered_df = df.copy()

if selected_media != "All":
    filtered_df = filtered_df[
        filtered_df["media_type"] == selected_media
    ]

with st.sidebar:
    st.html(
        f"""
        <div class="sidebar-summary">
            <div class="sidebar-summary-label">POSTS IN THIS VIEW</div>
            <div class="sidebar-summary-value">{len(filtered_df):,}</div>
            <div class="sidebar-summary-note">Showing {escape(str(selected_media).lower())} content</div>
        </div>
        """
    )

# KPI Cards
total_posts = len(filtered_df)
total_likes = filtered_df["likes"].sum()
total_reach = filtered_df["reach"].sum()
total_engagement = filtered_df["total_engagement"].sum()

st.html(
    f"""
    <div class="dashboard-section-heading">
        <div>
            <div class="dashboard-section-kicker">Performance overview</div>
            <h2>Your account at a glance</h2>
            <p>Key results for {escape(str(selected_media).lower())} content.</p>
        </div>
        <span class="dashboard-section-badge">{len(filtered_df):,} POSTS ANALYZED</span>
    </div>
    """
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Posts", f"{total_posts:,}")
col2.metric("Total Likes", f"{total_likes:,}")
col3.metric("Total Reach", f"{total_reach:,}")
col4.metric("Total Engagement", f"{total_engagement:,}")

st.divider()


def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#675665", family="Arial, sans-serif", size=12),
        margin=dict(l=24, r=24, t=24, b=24),
        height=340,
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="#5a1746",
            bordercolor="#d63378",
            font=dict(color="#ffffff", family="Arial, sans-serif"),
        ),
        hovermode="closest",
        transition=dict(duration=650, easing="cubic-in-out"),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#eed9e3",
        tickfont=dict(color="#796475"),
        title_font=dict(color="#796475"),
    )
    fig.update_yaxes(
        gridcolor="#f4e8ee",
        zerolinecolor="#f0dce6",
        tickfont=dict(color="#796475"),
        title_font=dict(color="#796475"),
    )
    return fig


# Chart 1: Media Type Performance
media_data = (
    filtered_df.groupby("media_type")["total_engagement"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    media_data,
    x="media_type",
    y="total_engagement",
    color="media_type",
    color_discrete_sequence=["#e1306c", "#c13584", "#833ab4", "#fd1d1d", "#f77737"],
)

style_chart(fig1)

# Chart 2: Content Category
category_data = (
    filtered_df.groupby("content_category")["total_engagement"]
    .sum()
    .reset_index()
    .sort_values("total_engagement", ascending=False)
)

fig2 = px.bar(
    category_data,
    x="content_category",
    y="total_engagement",
    color_discrete_sequence=["#d63378"],
)

style_chart(fig2)

st.html(
    """
    <div class="dashboard-section-heading">
        <div>
            <div class="dashboard-section-kicker">Explore your content</div>
            <h2>Find what resonates</h2>
            <p>Compare formats, themes, and timing to spot your strongest signals.</p>
        </div>
        <span class="dashboard-section-badge">ENGAGEMENT TRENDS</span>
    </div>
    """
)

chart_col1, chart_col2 = st.columns(2, gap="large")
with chart_col1:
    with st.container(border=True, key="chart-media"):
        st.subheader("Media type")
        st.caption("Which formats are earning the most interactions?")
        st.plotly_chart(
            fig1,
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )

with chart_col2:
    with st.container(border=True, key="chart-category"):
        st.subheader("Content category")
        st.caption("See which themes are connecting with your audience.")
        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displayModeBar": False, "scrollZoom": False},
        )

# Chart 3: Engagement by Posting Hour
hour_data = (
    filtered_df.groupby("post_hour")["total_engagement"]
    .sum()
    .reset_index()
    .sort_values("post_hour")
)

fig3 = px.line(
    hour_data,
    x="post_hour",
    y="total_engagement",
    markers=True,
    color_discrete_sequence=["#d63378"],
)

style_chart(fig3)
fig3.update_layout(height=380)
fig3.update_traces(
    line=dict(color="#d63378", width=3),
    marker=dict(color="#f0648b", size=9, line=dict(color="#ffffff", width=2)),
    hovertemplate="<b>Hour %{x}:00</b><br>Engagement %{y:,.0f}<extra></extra>",
)
st.write("")
with st.container(border=True, key="chart-hour"):
    st.subheader("Your audience's active hours")
    st.caption("Use this trend to spot time windows when your posts get noticed.")
    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
    )

# Data preview
with st.container(key="data-library"):
    st.html(
        f"""
        <div class="data-library-heading">
            <div>
                <div class="data-library-kicker">Your content library</div>
                <h2>Every post, in one place</h2>
                <p>Open a quick preview of your Instagram data.</p>
            </div>
            <span class="data-library-count">{len(filtered_df):,} POSTS</span>
        </div>
        """
    )
    with st.expander("Open post data preview"):
        st.caption(f"Showing the first {min(len(filtered_df), 100):,} of {len(filtered_df):,} posts in this view.")
        st.dataframe(filtered_df.head(100), use_container_width=True)
