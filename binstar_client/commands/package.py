'''
Binstar package utilities
'''
from __future__ import print_function
from binstar_client.utils import get_binstar, parse_specs
import logging

log = logging.getLogger('binstar.package')
def main(args):

    bs = get_binstar()
    spec = args.spec

    owner = spec.user
    package = spec.package

    if args.add_collaborator:
        collaborator = args.add_collaborator
        bs.package_add_collaborator(owner, package, collaborator)
        args.add_collaborator

    elif args.list_collaborators:
        log.info(':Collaborators:')
        for collab in binstar.package_collaborators(owner, package):
            log.info('   +', collab['login'])
    elif args.create:
        public = args.access != 'private'
        publish = args.access == 'publish'
        bs.add_package(args.spec.user, args.spec.package, args.summary,  
                       public=public, publish=publish, 
                       license=args.license, license_url=args.license_url)
        log.info('Package created!')

def add_parser(subparsers):

    parser = subparsers.add_parser('package',
                                      help='Package utils',
                                      description=__doc__)

    parser.add_argument('spec', help='Package to operate on', type=parse_specs)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--add-collaborator', metavar='user', help='username of the collaborator you want to add')
    group.add_argument('--list-collaborators', action='store_true', help='list all of the collaborators in a package')
    group.add_argument('--create', action='store_true', help='Create a package')
    
    parser.add_argument('--summary', help='Set the package short summary')
    parser.add_argument('--license', help='Set the package license')
    parser.add_argument('--license-url', help='Set the package license url')
    
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--publish', action='store_const', const='publish', dest='access',
                       help=('Set the package access to published. '
                             'The package name must not conflict with any other published package')
                       )
    group.add_argument('--personal', action='store_const', const='personal', dest='access',
                       help=('Set the package access to personal '
                             'This package will be available only on your personal regitries'))
    group.add_argument('--private', action='store_const', const='private', dest='access',
                       help=('Set the package access to private '
                             'This package will require authenticated access to install'))

    parser.set_defaults(main=main)
