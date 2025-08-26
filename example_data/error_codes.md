# Error Messages and Performance Issues

## ⛔ 503 Errors / Slow Site

- Your cPanel account may be hitting its resource limits (CPU, RAM, etc.).
- Please review this article to identify and fix the issue:
  [Identify and Fix Performance Issues on WordPress Site](https://middlehost.com/knowledgebase/books/shared-cloud-hosting/page/identify-and-fix-performance-issues-on-wordpress-site)

## 🌩 Cloudflare 520 / 502 Error Pages

- These errors usually indicate incorrect IP address settings in Cloudflare.
- Double-check and ensure that the A record points to your correct Middlehost server IP.

## 🚫 403 Forbidden Error

- Your IP address might be blocked by our security system.
- We use **Imunify360** which relies on the **RBL (Real-time Blackhole List)**.
- Try using any other internet connection. if problem is because of IP in RBL, this should fix the problem. If it does not create ticket.
- For more information, please read:
  [Questions and Answers about RBL](https://cloudlinux.zendesk.com/hc/en-us/articles/4407495008786-Questions-and-answers-about-RBL)
- If You're getting 403 when placing adsterra ads. Follow this guide: [Implementing Adsterra Code on WordPress](https://middlehost.com/knowledgebase/books/shared-cloud-hosting/page/implementing-adsterra-code-on-wordpress)
