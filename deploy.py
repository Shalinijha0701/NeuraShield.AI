import os
import subprocess

def deploy_neurashield():
    print("Deploying NeuraShield.AI...")
    
    # Create deployment files
    print("1. Creating deployment files...")
    
    # Vercel deployment
    vercel_config = '''{
  "name": "neurashield-ai",
  "version": 2,
  "builds": [
    { "src": "index.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}'''
    
    with open('vercel.json', 'w') as f:
        f.write(vercel_config)
    
    # Netlify deployment
    netlify_config = '''[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200'''
    
    with open('netlify.toml', 'w') as f:
        f.write(netlify_config)
    
    print("2. Deployment options:")
    print("   A. GitHub Pages (Free)")
    print("   B. Vercel (Free)")
    print("   C. Netlify (Free)")
    print("   D. Local Server")
    
    choice = input("Choose option (A/B/C/D): ").upper()
    
    if choice == 'A':
        deploy_github()
    elif choice == 'B':
        deploy_vercel()
    elif choice == 'C':
        deploy_netlify()
    elif choice == 'D':
        deploy_local()

def deploy_github():
    print("GitHub Pages deployment:")
    print("1. Create GitHub repo")
    print("2. Upload files")
    print("3. Enable Pages in Settings")
    print("4. Your site: https://username.github.io/neurashield-ai")

def deploy_vercel():
    print("Vercel deployment:")
    print("1. Install: npm i -g vercel")
    print("2. Run: vercel")
    print("3. Follow prompts")
    print("4. Live URL provided")

def deploy_netlify():
    print("Netlify deployment:")
    print("1. Go to netlify.com")
    print("2. Drag & drop project folder")
    print("3. Instant deployment")
    print("4. Custom domain available")

def deploy_local():
    print("Starting local server...")
    try:
        subprocess.run(['python', '-m', 'http.server', '3000'], cwd='.')
    except:
        subprocess.run(['py', '-m', 'http.server', '3000'], cwd='.')

if __name__ == "__main__":
    deploy_neurashield()