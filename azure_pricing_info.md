# Azure App Service Pricing Information

## Free Plan (F1)
- **Cost**: $0 (Free)
- **Cores**: Shared (60 CPU minutes / day)
- **RAM**: 1 GB
- **Storage**: 1.00 GB
- **Limitations**: 
  - No SLA for free plan
  - Metered on a per app basis
  - Use of free plan for production workloads is not supported
  - Intended for trials, experimentation, and learning

## Basic Plans
- **B1**: 1 core, 1.75 GB RAM, 10 GB storage - $13.140/month
- **B2**: 2 cores, 3.50 GB RAM, 10 GB storage - $25.55/month
- **B3**: 4 cores, 7 GB RAM, 10 GB storage - $51.10/month

## Key Points for Our Deployment
1. The Free plan (F1) is suitable for development and testing
2. Limited to 60 CPU minutes per day
3. 1 GB RAM and 1 GB storage should be sufficient for our SAGE EFL system
4. No cost involved for initial deployment and testing
5. Can upgrade to paid plans if needed for production use

## Deployment Strategy
- Start with Free plan for initial deployment
- Monitor usage and performance
- Upgrade to Basic plan if needed for production use
- Consider the 60 CPU minutes/day limitation for user activity planning

