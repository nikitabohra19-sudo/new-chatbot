"""Seed database with 65+ AI tools and categories."""
from models import get_db, create_tables

CATEGORIES = [
    ('Writing', '✍️', 'AI writing assistants and content generators'),
    ('Image', '🎨', 'AI image generation and editing tools'),
    ('Code', '💻', 'AI coding assistants and dev tools'),
    ('Video', '🎬', 'AI video creation and editing'),
    ('Audio', '🎵', 'AI voice, music, and audio tools'),
    ('Productivity', '⚡', 'AI tools to boost your workflow'),
    ('Design', '🎯', 'AI design and creative tools'),
    ('Research', '🔬', 'AI research and analysis tools'),
    ('Marketing', '📢', 'AI marketing and SEO tools'),
    ('Education', '📚', 'AI learning and tutoring tools'),
    ('Business', '💼', 'AI tools for business and finance'),
    ('Data', '📊', 'AI data analysis and visualization'),
]

TOOLS = [
    # ── Writing (8 tools) ──
    ('ChatGPT', 'Your AI conversation partner', 'The most popular AI chatbot by OpenAI. Great for writing, brainstorming, coding help, and answering questions. Very easy to use for beginners.', 'Writing', 4.8, 'Freemium', 'https://chat.openai.com', '🤖', 'Natural conversation,Code generation,Content writing,Translation,Image generation', 'Blog posts,Emails,Study help,Brainstorming,Summarizing', 1, 0),
    ('Claude', 'Thoughtful AI assistant', 'Made by Anthropic. Known for long, detailed, and safe responses. Great for analysis, writing, and complex reasoning tasks.', 'Writing', 4.7, 'Freemium', 'https://claude.ai', '🧠', 'Long context,Analysis,Safe responses,Document reading,Coding', 'Research papers,Long documents,Creative writing,Data analysis', 1, 0),
    ('Jasper', 'AI marketing copywriter', 'Specialized AI for marketing copy. Creates ads, blog posts, social media captions, and product descriptions in seconds.', 'Writing', 4.5, 'Paid', 'https://jasper.ai', '📝', 'Marketing copy,Brand voice,Templates,SEO writing,Campaigns', 'Ad copy,Blog posts,Social media,Product descriptions', 0, 0),
    ('Copy.ai', 'Free AI copywriting tool', 'Generates marketing copy, blog intros, product descriptions, and social posts. Has a generous free plan for beginners.', 'Writing', 4.3, 'Freemium', 'https://copy.ai', '📋', 'Quick copy,Templates,Free tier,Multiple languages', 'Social media posts,Email subjects,Blog intros,Taglines', 0, 0),
    ('Writesonic', 'AI writer for everyone', 'Creates blog posts, ads, and landing pages. Includes an AI article writer and a chatbot called Chatsonic.', 'Writing', 4.2, 'Freemium', 'https://writesonic.com', '✏️', 'Article writer,Chatsonic,Landing pages,Paraphrasing', 'Full articles,Facebook ads,Landing pages,Paraphrasing', 0, 1),
    ('Rytr', 'Affordable AI writer', 'Budget-friendly AI writing assistant. Generate blogs, emails, and ad copy in 30+ languages. Great free plan.', 'Writing', 4.1, 'Freemium', 'https://rytr.me', '✨', 'Free plan,30+ languages,Tone selection,Use cases', 'Blog posts,Emails,Social media,Product descriptions', 0, 0),
    ('Sudowrite', 'AI for fiction writers', 'AI writing tool specifically designed for novelists and fiction writers. Helps with plot, character development, and prose.', 'Writing', 4.3, 'Paid', 'https://sudowrite.com', '📖', 'Fiction writing,Plot generation,Character building,Style matching', 'Novels,Short stories,Screenplays,Creative fiction', 0, 1),
    ('Wordtune', 'AI rewriting assistant', 'Rewrites sentences to make them clearer, more engaging, or more formal. Integrates right into your browser.', 'Writing', 4.2, 'Freemium', 'https://wordtune.com', '🔄', 'Sentence rewriting,Tone adjustment,Browser extension,Summarizer', 'Emails,Reports,Academic writing,Business docs', 0, 0),

    # ── Image (8 tools) ──
    ('Midjourney', 'Stunning AI art generator', 'Creates beautiful, artistic images from text descriptions. Used by professionals and artists worldwide. Works inside Discord.', 'Image', 4.9, 'Paid', 'https://midjourney.com', '🎨', 'Photorealistic art,Styles,Variations,Upscaling', 'Concept art,Marketing images,Social media,Illustrations', 1, 0),
    ('DALL-E 3', 'OpenAI image generator', 'Built into ChatGPT. Creates images from text prompts with great accuracy. Very beginner-friendly.', 'Image', 4.6, 'Freemium', 'https://openai.com/dall-e-3', '🖼️', 'Text-to-image,Editing,Variations,ChatGPT integrated', 'Social media graphics,Presentations,Concept art,Logos', 1, 0),
    ('Leonardo AI', 'AI art with fine control', 'Powerful free AI image generator with lots of style options. Great for game assets and illustrations.', 'Image', 4.5, 'Freemium', 'https://leonardo.ai', '🦁', 'Fine-tuned models,Game assets,Realtime canvas,Free tier', 'Game art,Characters,Textures,Marketing images', 0, 1),
    ('Stable Diffusion', 'Open-source AI images', 'Free and open-source image generator. Run it on your own computer or use online. Most customizable.', 'Image', 4.4, 'Free', 'https://stability.ai', '🌀', 'Open source,Local running,LoRA training,Inpainting', 'Custom art,Photo editing,Batch generation,Research', 0, 0),
    ('Adobe Firefly', 'AI for creative pros', 'Adobe AI image generation. Trained on licensed content, safe for commercial use.', 'Image', 4.5, 'Freemium', 'https://firefly.adobe.com', '🔥', 'Commercial safe,Photoshop integration,Text effects,Generative fill', 'Product photos,Marketing,Social media,Design', 0, 1),
    ('Ideogram', 'AI images with perfect text', 'Generates images with readable, accurate text. Perfect for posters, logos, and social media graphics.', 'Image', 4.4, 'Freemium', 'https://ideogram.ai', '💎', 'Text in images,Poster design,Logo generation,High quality', 'Posters,Social graphics,Logos,Marketing materials', 0, 1),
    ('Flux', 'Next-gen image model', 'Open-source image model by Black Forest Labs. Produces extremely high quality, photorealistic images.', 'Image', 4.6, 'Free', 'https://blackforestlabs.ai', '⚡', 'Photorealistic,Open source,Fast generation,High resolution', 'Photography,Art,Marketing,Product photos', 1, 1),
    ('Playground AI', 'Free AI image playground', 'Free tool to generate and edit images. Mix styles, use templates, and create social media graphics easily.', 'Image', 4.2, 'Freemium', 'https://playground.com', '🎮', 'Free generation,Mixed styles,Templates,Social graphics', 'Social media,Creative projects,Experiments,Learning', 0, 0),

    # ── Code (7 tools) ──
    ('GitHub Copilot', 'AI pair programmer', 'Suggests code as you type in your editor. Supports all major languages. Like having a coding partner.', 'Code', 4.7, 'Paid', 'https://github.com/features/copilot', '👨‍💻', 'Code completion,Multi-language,IDE integration,Code explanation', 'Writing code,Bug fixing,Learning to code,Refactoring', 1, 0),
    ('Cursor', 'AI-first code editor', 'A code editor built around AI. Chat with your codebase, generate features, fix bugs.', 'Code', 4.8, 'Freemium', 'https://cursor.com', '🖱️', 'AI code editor,Chat with code,Multi-file edit,Bug fixing', 'Full projects,Debugging,Refactoring,Learning', 1, 1),
    ('Replit', 'AI cloud coding platform', 'Code in your browser with AI help. No setup needed. Great for beginners and quick projects.', 'Code', 4.4, 'Freemium', 'https://replit.com', '💡', 'Browser IDE,AI assistant,Deploy instantly,Collaborative', 'Learning to code,Prototypes,Web apps,Bots', 0, 0),
    ('Codeium', 'Free AI code completion', 'Free alternative to GitHub Copilot. Autocompletes code in 70+ languages.', 'Code', 4.3, 'Free', 'https://codeium.com', '⚡', 'Free forever,70+ languages,IDE plugins,Code chat', 'Code completion,Learning,Side projects,Students', 0, 0),
    ('Tabnine', 'AI code completions', 'AI coding assistant that runs locally for privacy. Supports all major IDEs and languages.', 'Code', 4.2, 'Freemium', 'https://tabnine.com', '🔐', 'Local AI,Privacy first,IDE support,Team features', 'Enterprise code,Private repos,Secure development', 0, 0),
    ('Bolt.new', 'AI full-stack builder', 'Build and deploy full-stack web apps by just describing them. AI writes the code for you.', 'Code', 4.5, 'Freemium', 'https://bolt.new', '⚡', 'Full-stack,Deploy instantly,No setup,Natural language', 'Web apps,Prototypes,MVPs,Landing pages', 1, 1),
    ('v0 by Vercel', 'AI UI component builder', 'Generate React UI components with AI. Describe the UI you want and it builds the code.', 'Code', 4.4, 'Freemium', 'https://v0.dev', '🎯', 'React components,UI generation,Shadcn,Tailwind', 'UI components,Dashboards,Landing pages,Forms', 0, 1),

    # ── Video (7 tools) ──
    ('Runway', 'AI video creation suite', 'Professional AI video tools. Generate videos from text, used in Hollywood movies.', 'Video', 4.6, 'Freemium', 'https://runwayml.com', '🎬', 'Text-to-video,Gen-3,Background removal,Motion brush', 'Short films,Social content,Ads,Music videos', 1, 0),
    ('Synthesia', 'AI avatar videos', 'Create videos with AI presenters. No camera needed. Over 150 avatars available.', 'Video', 4.5, 'Paid', 'https://synthesia.io', '🧑‍💼', 'AI avatars,150+ languages,Script to video,Custom avatars', 'Training videos,Marketing,Presentations,Education', 0, 0),
    ('HeyGen', 'AI spokesperson videos', 'Create professional videos with AI avatars quickly. Popular for marketing and social.', 'Video', 4.4, 'Freemium', 'https://heygen.com', '👤', 'Instant avatars,Lip sync,Templates,Translation', 'Product demos,Social media,E-commerce,Training', 0, 1),
    ('Pika', 'Fun AI video generator', 'Create and edit short videos with AI. Simple interface for creative experiments.', 'Video', 4.2, 'Freemium', 'https://pika.art', '⚡', 'Text-to-video,Image-to-video,Editing,Effects', 'Social clips,Animations,Creative,Experiments', 0, 1),
    ('Luma Dream Machine', 'Photorealistic AI video', 'Generates high-quality, realistic videos from text and images. Very fast generation.', 'Video', 4.5, 'Freemium', 'https://lumalabs.ai/dream-machine', '🌟', 'Realistic video,Fast generation,Image-to-video,Camera motion', 'Product videos,Social content,Concept videos,Art', 1, 1),
    ('Kling AI', 'Long AI video generator', 'Chinese AI video generator that creates high-quality, longer video clips with great motion.', 'Video', 4.3, 'Freemium', 'https://klingai.com', '🎥', 'Long videos,High quality,Motion control,Effects', 'Short films,Music videos,Ads,Social media', 0, 1),
    ('Descript', 'AI video editing made easy', 'Edit videos as easily as editing a document. Remove filler words, clone your voice, add captions.', 'Video', 4.5, 'Freemium', 'https://descript.com', '✂️', 'Text-based editing,Filler word removal,Screen recording,Transcripts', 'Podcasts,YouTube videos,Presentations,Courses', 0, 0),

    # ── Audio (6 tools) ──
    ('ElevenLabs', 'Realistic AI voices', 'Best-in-class AI voice generator. Clone voices, create audiobooks, add voiceover. Sounds incredibly human.', 'Audio', 4.8, 'Freemium', 'https://elevenlabs.io', '🎙️', 'Voice cloning,29 languages,Audiobooks,API access', 'Voiceovers,Audiobooks,Podcasts,Videos', 1, 0),
    ('Suno', 'AI music generator', 'Create full songs with AI — lyrics, vocals, instruments. Just describe the song you want.', 'Audio', 4.6, 'Freemium', 'https://suno.com', '🎶', 'Full songs,Lyrics,Multiple genres,Vocals', 'Background music,Songs,Jingles,Experiments', 1, 1),
    ('Murf AI', 'AI voiceover studio', 'Professional voiceovers in minutes. 120+ voices in 20+ languages.', 'Audio', 4.3, 'Freemium', 'https://murf.ai', '🔊', '120+ voices,20 languages,Studio editor,Tone control', 'Presentations,Training,Ads,YouTube', 0, 0),
    ('Udio', 'AI music creation', 'Create original music tracks with AI. High-quality audio generation with genre control.', 'Audio', 4.5, 'Freemium', 'https://udio.com', '🎵', 'Music generation,Genre control,High quality,Lyrics', 'Music production,Background tracks,Jingles,Podcasts', 0, 1),
    ('AIVA', 'AI music composer', 'AI composer for soundtracks and background music. Used in films, games, and ads.', 'Audio', 4.2, 'Freemium', 'https://aiva.ai', '🎼', 'Soundtrack generation,Emotional AI,Film scores,Customizable', 'Film music,Game soundtracks,Ads,Relaxation', 0, 0),
    ('Speechify', 'AI text-to-speech reader', 'Reads any text aloud with natural voices. Great for students, professionals, and accessibility.', 'Audio', 4.4, 'Freemium', 'https://speechify.com', '📢', 'Text-to-speech,Natural voices,PDF reading,Chrome extension', 'Reading articles,Studying,Accessibility,Multitasking', 0, 0),

    # ── Productivity (7 tools) ──
    ('Notion AI', 'AI-powered workspace', 'Adds AI to your Notion workspace. Summarize notes, generate content, create action items.', 'Productivity', 4.6, 'Paid', 'https://notion.so/product/ai', '📓', 'Summarization,Writing,Brainstorming,Action items', 'Notes,Project plans,Meeting notes,Knowledge base', 1, 0),
    ('Grammarly', 'AI writing assistant', 'Checks grammar, spelling, tone, and style. Works everywhere you write. Essential tool.', 'Productivity', 4.7, 'Freemium', 'https://grammarly.com', '✅', 'Grammar check,Tone detection,Plagiarism,AI writing', 'Emails,Documents,Social media,Academic papers', 1, 0),
    ('Otter.ai', 'AI meeting notes', 'Records and transcribes meetings automatically. Generates summaries and action items.', 'Productivity', 4.4, 'Freemium', 'https://otter.ai', '🦦', 'Transcription,Meeting summary,Action items,Search', 'Meetings,Interviews,Lectures,Podcasts', 0, 0),
    ('Gamma', 'AI presentation maker', 'Create beautiful presentations in seconds. Describe your topic and AI builds the slides.', 'Productivity', 4.5, 'Freemium', 'https://gamma.app', '📊', 'AI slides,Beautiful design,One-click,Export options', 'Presentations,Pitch decks,Reports,Proposals', 0, 1),
    ('Mem', 'AI-powered notes', 'Self-organizing note-taking app. AI finds connections between your notes and surfaces relevant info.', 'Productivity', 4.2, 'Freemium', 'https://mem.ai', '🧠', 'Self-organizing,AI search,Smart suggestions,Connections', 'Personal notes,Research,Ideas,Knowledge management', 0, 1),
    ('Reclaim AI', 'AI calendar assistant', 'Automatically schedules meetings, focus time, and habits. Optimizes your calendar with AI.', 'Productivity', 4.3, 'Freemium', 'https://reclaim.ai', '📅', 'Smart scheduling,Habit tracking,Focus time,Team sync', 'Calendar management,Time blocking,Meetings,Productivity', 0, 0),
    ('Fireflies.ai', 'AI meeting recorder', 'Records, transcribes, and summarizes meetings. Integrates with Zoom, Teams, and Google Meet.', 'Productivity', 4.4, 'Freemium', 'https://fireflies.ai', '🪄', 'Meeting recording,Transcription,Summaries,Integrations', 'Team meetings,Interviews,Sales calls,Brainstorms', 0, 0),

    # ── Design (5 tools) ──
    ('Canva AI', 'AI-powered design platform', 'Design anything with AI help — presentations, social posts, logos, videos.', 'Design', 4.7, 'Freemium', 'https://canva.com', '🎯', 'Magic Design,Text-to-image,Background removal,Templates', 'Social media,Presentations,Marketing,Posters', 1, 0),
    ('Figma AI', 'AI for UI/UX design', 'AI features built into Figma for designers. Auto-layout, generate components.', 'Design', 4.5, 'Freemium', 'https://figma.com', '🖌️', 'Auto-layout,Component generation,UI design,Prototyping', 'App design,Websites,Prototypes,Design systems', 0, 1),
    ('Framer', 'AI website builder', 'Build and publish professional websites with AI. No coding required.', 'Design', 4.5, 'Freemium', 'https://framer.com', '🌐', 'AI website builder,CMS,Animations,SEO', 'Portfolios,Landing pages,Business sites,Blogs', 0, 1),
    ('Looka', 'AI logo maker', 'Design professional logos with AI. Just enter your brand name and preferences.', 'Design', 4.2, 'Paid', 'https://looka.com', '🏷️', 'Logo design,Brand kits,Business cards,Social media', 'Startups,Small business,Personal brands,Side projects', 0, 0),
    ('Khroma', 'AI color palette generator', 'AI learns your color preferences and generates beautiful palettes you will love.', 'Design', 4.1, 'Free', 'https://khroma.co', '🎨', 'Color palettes,AI learning,Favorites,Export', 'Web design,Brand colors,Interior design,Art', 0, 0),

    # ── Research (5 tools) ──
    ('Perplexity', 'AI-powered search engine', 'Ask questions and get detailed answers with sources. Like Google but it reads for you.', 'Research', 4.7, 'Freemium', 'https://perplexity.ai', '🔍', 'Web search,Sources,Follow-up questions,Pro search', 'Research,Fact-checking,Learning,News', 1, 0),
    ('Consensus', 'AI for research papers', 'Search 200M+ research papers with AI. Get evidence-based answers from scientific studies.', 'Research', 4.4, 'Freemium', 'https://consensus.app', '📊', 'Paper search,Evidence meter,Citations,Summaries', 'Academic research,Literature review,Fact-checking,Students', 0, 0),
    ('Elicit', 'AI research assistant', 'Finds relevant papers, extracts key findings, and summarizes research.', 'Research', 4.3, 'Freemium', 'https://elicit.com', '🧪', 'Paper discovery,Data extraction,Summarization,Tables', 'Literature review,Thesis,Research,Analysis', 0, 0),
    ('Scite', 'Smart citation analysis', 'Shows how a paper has been cited — whether supporting, contrasting, or mentioning it.', 'Research', 4.2, 'Paid', 'https://scite.ai', '📑', 'Citation analysis,Smart citations,Paper search,Dashboards', 'Academic research,Citation tracking,Literature review', 0, 0),
    ('Connected Papers', 'Visual paper explorer', 'Visualize related research papers as an interactive graph. Great for literature reviews.', 'Research', 4.3, 'Freemium', 'https://connectedpapers.com', '🕸️', 'Graph visualization,Related papers,Export,Free tier', 'Literature review,Research,Thesis,Discovery', 0, 0),

    # ── Marketing (5 tools) ──
    ('Surfer SEO', 'AI SEO optimizer', 'Analyzes top-ranking pages and tells you how to optimize your content for search engines.', 'Marketing', 4.5, 'Paid', 'https://surferseo.com', '🏄', 'Content scoring,Keyword research,SERP analysis,AI writing', 'Blog SEO,Content strategy,Keyword planning,Optimization', 0, 0),
    ('Manychat', 'AI chatbot for business', 'Build chatbots for Instagram, WhatsApp, and Messenger. Automate conversations and sales.', 'Marketing', 4.4, 'Freemium', 'https://manychat.com', '💬', 'Instagram DMs,WhatsApp,Templates,Flow builder', 'Lead generation,Customer support,Sales,Engagement', 0, 1),
    ('Synthflow', 'AI phone calling agent', 'AI makes and answers phone calls for your business. Books appointments and qualifies leads.', 'Marketing', 4.2, 'Paid', 'https://synthflow.ai', '📞', 'AI phone calls,Appointment booking,Lead qualification,24/7', 'Sales calls,Customer service,Booking,Follow-ups', 0, 1),
    ('Instantly', 'AI email outreach', 'Send cold emails at scale with AI personalization. Warms up email accounts automatically.', 'Marketing', 4.3, 'Paid', 'https://instantly.ai', '📧', 'Cold email,AI warmup,Personalization,Analytics', 'Lead generation,Sales outreach,Recruitment,PR', 0, 0),
    ('AdCreative.ai', 'AI ad design', 'Generate high-converting ad creatives with AI. Creates banner ads, social ads, and copy.', 'Marketing', 4.3, 'Paid', 'https://adcreative.ai', '📱', 'Ad generation,Social ads,Performance scoring,A/B testing', 'Facebook ads,Google ads,Instagram,Banner ads', 0, 0),

    # ── Education (5 tools) ──
    ('Khan Academy Khanmigo', 'AI tutor by Khan Academy', 'Free AI tutor that helps students learn by asking guiding questions. Safe and educational.', 'Education', 4.6, 'Free', 'https://khanacademy.org/khan-labs', '🎓', 'Tutoring,Step-by-step,Safe for kids,All subjects', 'Math help,Science,Homework,Test prep', 0, 1),
    ('Duolingo Max', 'AI language learning', 'Adds AI conversations and explanations to Duolingo. Practice speaking with AI.', 'Education', 4.5, 'Paid', 'https://duolingo.com', '🦉', 'AI conversations,Explanations,40+ languages,Gamified', 'Language learning,Speaking practice,Grammar,Vocabulary', 0, 0),
    ('Quillbot', 'AI paraphrasing tool', 'Rewrite text in different styles — formal, casual, simple, creative. Great for students.', 'Education', 4.3, 'Freemium', 'https://quillbot.com', '🪶', 'Paraphrasing,Summarizing,Grammar check,Co-writer', 'Essays,Reports,Emails,Academic writing', 0, 0),
    ('Photomath', 'AI math solver', 'Point your camera at a math problem and get step-by-step solutions. Covers algebra through calculus.', 'Education', 4.5, 'Freemium', 'https://photomath.com', '📸', 'Camera scan,Step-by-step,All math levels,Graphs', 'Homework help,Test prep,Math practice,Learning', 0, 0),
    ('Socratic by Google', 'AI homework helper', 'Ask any homework question and get explanations with visuals. Free by Google.', 'Education', 4.3, 'Free', 'https://socratic.org', '🎒', 'Homework help,Visual explanations,Free,Multiple subjects', 'Science,Math,Literature,History', 0, 0),

    # ── Business (5 tools) ──
    ('Beautiful.ai', 'AI presentation tool', 'Creates stunning business presentations with smart formatting. Teams love it for pitch decks.', 'Business', 4.4, 'Paid', 'https://beautiful.ai', '📊', 'Smart slides,Team collaboration,Templates,Brand kit', 'Pitch decks,Reports,Proposals,Team meetings', 0, 0),
    ('Tome', 'AI storytelling presentations', 'Creates narrative presentations with AI-generated text and images. Tell your story visually.', 'Business', 4.3, 'Freemium', 'https://tome.app', '📕', 'Narrative format,AI images,One-click generation,Sharing', 'Sales decks,Project updates,Creative briefs,Portfolios', 0, 1),
    ('Loom AI', 'AI video messaging', 'Record and share video messages with auto-generated titles, summaries, and chapters.', 'Business', 4.5, 'Freemium', 'https://loom.com', '📹', 'Screen recording,AI summaries,Auto chapters,CTAs', 'Team updates,Tutorials,Bug reports,Sales messages', 0, 0),
    ('Mixo', 'AI website builder for startups', 'Launch a website in seconds by describing your startup idea. AI writes content and designs layout.', 'Business', 4.1, 'Paid', 'https://mixo.io', '🚀', 'Instant website,AI content,Subscriber collection,SEO', 'Landing pages,MVPs,Idea validation,Startups', 0, 1),
    ('Rows', 'AI spreadsheet', 'Spreadsheet with built-in AI. Analyze data, generate charts, and automate tasks with natural language.', 'Business', 4.2, 'Freemium', 'https://rows.com', '📈', 'AI formulas,Data analysis,Charts,Integrations', 'Financial analysis,Reporting,Data tracking,Dashboards', 0, 0),

    # ── Data (4 tools) ──
    ('Julius AI', 'AI data analyst', 'Upload your data and ask questions in plain English. Creates charts, finds patterns, and explains insights.', 'Data', 4.4, 'Freemium', 'https://julius.ai', '📊', 'Natural language queries,Charts,Data cleaning,Export', 'Data analysis,Reports,Visualization,Insights', 0, 1),
    ('Hex', 'AI-powered analytics', 'Collaborative data workspace with AI. Write SQL, Python, and create dashboards with AI help.', 'Data', 4.3, 'Freemium', 'https://hex.tech', '🔮', 'SQL generation,Python notebooks,Dashboards,Collaboration', 'Analytics,Data science,Reporting,Team analysis', 0, 0),
    ('Akkio', 'No-code AI for data', 'Build AI models without coding. Predict outcomes, forecast trends, and classify data easily.', 'Data', 4.2, 'Paid', 'https://akkio.com', '🤖', 'No-code ML,Predictions,Forecasting,Integrations', 'Sales forecasting,Churn prediction,Lead scoring,Trends', 0, 0),
    ('Obviously AI', 'AI predictions made easy', 'No-code platform for building prediction models. Upload a CSV and get predictions instantly.', 'Data', 4.1, 'Paid', 'https://obviously.ai', '🎯', 'No-code predictions,CSV upload,Auto ML,Reports', 'Revenue prediction,Customer analysis,Risk assessment', 0, 0),
]

def seed():
    create_tables()
    db = get_db()
    for t in ['tools', 'categories', 'notifications']:
        db.execute(f'DELETE FROM {t}')
    for name, icon, desc in CATEGORIES:
        db.execute('INSERT INTO categories (name, icon, description) VALUES (?, ?, ?)', (name, icon, desc))
    for t in TOOLS:
        db.execute('''INSERT INTO tools (name, tagline, description, category, rating, pricing, url, logo, features, use_cases, is_trending, is_new)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', t)
    for name, _, _ in CATEGORIES:
        count = db.execute('SELECT COUNT(*) FROM tools WHERE category = ?', (name,)).fetchone()[0]
        db.execute('UPDATE categories SET tool_count = ? WHERE name = ?', (count, name))
    db.commit()
    db.close()
    print(f"[OK] Seeded {len(CATEGORIES)} categories and {len(TOOLS)} tools!")

if __name__ == '__main__':
    seed()
