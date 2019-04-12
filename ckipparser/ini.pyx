# -*- coding:utf-8 -*-
# cython: language_level=3

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'


def create_parser_ini(*, wsinifile, ruledir=None, rdbdir=None, do_ws=True, do_parse=True, do_role=True, **options):
	"""Generate CKIP parser config.

	Args:
		ruledir (str): the path to "Rule/".
		rdbdir (str):  the path to "RDB/".

		do_ws (bool):    do word-segmentation.
		do_parse (bool): do parsing.
		do_role (bool):  do role.
	"""
	if ruledir is None:
		ruledir = __os.getenv('CKIPPARSER_RULE')
		if not ruledir:
			ruledir = __os.path.join(__sys.prefix, 'share', 'pyckip', 'Rule')
		if not __os.path.isdir(ruledir):
			print('Warning: invalid ruledir (%s)')
			ruledir = 'Rule'

	if rdbdir is None:
		rdbdir = __os.getenv('CKIPPARSER_RDB')
		if not rdbdir:
			rdbdir = __os.path.join(__sys.prefix, 'share', 'pyckip', 'RDB')
		if not __os.path.isdir(rdbdir):
			print('Warning: invalid rdbdir (%s)')
			rdbdir = 'RDB'

	IsTag          = not do_ws
	AssignRole     = do_role
	AssignRoleOnly = False

	if not do_parse:
		if not do_ws and not do_role:
			raise ValueError('Must select at least one task')
		if do_ws and not do_role:
			raise ValueError('Use ckipws.CkipWS for word-segmentation')
		if not do_ws and do_role:
			AssignRoleOnly = True
		if do_ws and do_role:
			raise ValueError('Invalid tasks')

	cfg = []

	cfg.append(';PyCkip {version}'.format(version=__version__))
	cfg.append(';parser.ini')
	cfg.append(';Auto-generated {date}'.format(date=__datetime.datetime.now()))
	cfg.append('')

	cfg.append('[WordSeg]')
	cfg.append('ini={wsinifile}'.format(wsinifile=wsinifile))
	cfg.append('')

	cfg.append('[Parser]')
	cfg.append('SetPos13=0')
	cfg.append('13CateFile={ruledir}/13Cate.txt'.format(ruledir=ruledir))
	cfg.append('')

	# cfg.append('SetMap=1')
	cfg.append('SetMap=0')
	cfg.append('CatMapFile={ruledir}/CatMap.txt'.format(ruledir=ruledir))
	cfg.append('')

	cfg.append('GrammarRule={ruledir}/CKIP-Rule.txt'.format(ruledir=ruledir))
	cfg.append('HeadRule={ruledir}/CKIP-Head.txt'.format(ruledir=ruledir))
	cfg.append('')

	cfg.append('SetChangePos=1')
	cfg.append('SentenceDelimiter=，,；。！？')
	cfg.append('SetLength=15')
	cfg.append('NormalPos=1')
	cfg.append('NormalTree=1')
	cfg.append('IsTag={IsTag}'.format(IsTag=int(IsTag)))
	cfg.append('')

	cfg.append('[SRL]')
	cfg.append('DataPath={rdbdir}/'.format(rdbdir=rdbdir))
	cfg.append('AssignRole={AssignRole}'.format(AssignRole=int(AssignRole)))
	cfg.append('AssignRoleOnly={AssignRoleOnly}'.format(AssignRoleOnly=int(AssignRoleOnly)))

	return '\n'.join(cfg), options
