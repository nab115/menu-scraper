from distutils.core import setup
setup(
  name = 'menu_scraper',
  packages = ['menu_scraper'], 
  version = '0.1',
  license='MIT',
  description = 'tool for scraping menu items from restaurant websites',
  author = 'Naran Babha',
  author_email = 'nbabha@gmail.com',
  url = 'https://www.menu-monster.com/scraper',
  download_url = 'https://github.com/nab115/menu-scraper/archive/refs/tags/v1.0.0.tar.gz',    # I explain this later on
  keywords = ['webscraper', 'restaurant', 'menu items'],
  install_requires=[            # I get to this in a second
          'selenium',
          'beautifulsoup4',
          'pymongo',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)