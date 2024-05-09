# Vendor Management System with Performance Metrics

## Overview
This Vendor Management System (VMS) is built using Django and Django REST Framework. The system is designed to efficiently manage vendor profiles, track purchase orders, and calculate vendor performance metrics. It provides a user-friendly interface for administrators to handle various vendor-related tasks effectively.

## Core Features
1. **Vendor Profiles:** Create, update, and view vendor profiles with detailed information such as contact details, product offerings, and contract terms.

2. **Purchase Order Tracking:** Track purchase orders placed with vendors, including order details, delivery status, and payment information.

3. **Vendor Performance Metrics:** Automatically calculate and analyze vendor performance metrics based on factors such as delivery time, product quality, and adherence to contract terms.

4. **Real-time Updates:** Utilize Django signals to trigger metric updates in real-time when related purchase order data is modified. This ensures that performance metrics are always up-to-date and accurately reflect the current state of purchase orders.
