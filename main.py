# Copyright (C) 2016 0x9fff00

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse, json, os, random, shutil, uuid, zipfile

def move_texture(pc_texture, pe_texture):
    if os.path.isfile(pc_texture):
        os.rename(pc_texture, pe_texture)

parser = argparse.ArgumentParser(description='Convert Minecraft PC .zip resource packs to PE/Win10 .mcpack resource packs.')
parser.add_argument('input', help='Input .zip file')
parser.add_argument('output', help='Output .mcpack file (default: input with .mcpack extension)', nargs='?')
parser.add_argument('--name', help='Recource pack name (default: input file name)')
parser.add_argument('--version', help='Recource pack version (default: 0.1)')
parser.add_argument('--description', help='Recource pack description (default: copy from pack.mcmeta)')
parser.add_argument('--pack_id', help='Pack UUID')
parser.add_argument('--uuid', help='Module UUID')
args = parser.parse_args()

in_dir = 'tempin' + str(random.randint(0, 1000000))
in_zip = zipfile.ZipFile(args.input)
in_zip.extractall(in_dir)
in_zip.close()

if args.name == None:
    args.name = os.path.splitext(args.input)[0]

if args.version == None:
    args.version = "0.1"

if args.description == None:
    with open(in_dir + '/pack.mcmeta') as mcmeta_json:
        mcmeta = json.loads(mcmeta_json.read())
        args.description = mcmeta['pack']['description']

if args.pack_id == None:
    args.pack_id = str(uuid.uuid4())

if args.uuid == None:
    args.uuid = str(uuid.uuid4())

if args.output == None:
    args.output = os.path.splitext(args.input)[0] + '.mcpack'

print('Name: ' + args.name)
print('Version: ' + args.version)
print('Description: ' + args.description)
print('Pack UUID: ' + args.pack_id)
print('Module UUID: ' + args.uuid)

out_dir = 'tempout' + str(random.randint(0, 1000000))
shutil.copytree(in_dir + '/assets/minecraft/', out_dir) # textures
shutil.copyfile(in_dir + '/pack.png', out_dir + '/pack_icon.png') # icon

pack_manifest = {
    'header': {
        'pack_id': args.pack_id,
        'name': args.name,
        'packs_version': args.version,
        'description': args.description,
        'modules': [
            {
                'description': args.description,
                'version': args.version,
                'uuid': args.uuid,
                'type': 'resources'
            }
        ]
    }
}

json.dump(pack_manifest, open(out_dir + '/pack_manifest.json', 'w')) # pack manifest

os.chdir(out_dir + '/textures/')
move_texture('block/destroy_stage_0.png', 'environment/destroy_stage_0.png')
move_texture('block/destroy_stage_1.png', 'environment/destroy_stage_1.png')
move_texture('block/destroy_stage_2.png', 'environment/destroy_stage_2.png')
move_texture('block/destroy_stage_3.png', 'environment/destroy_stage_3.png')
move_texture('block/destroy_stage_4.png', 'environment/destroy_stage_4.png')
move_texture('block/destroy_stage_5.png', 'environment/destroy_stage_5.png')
move_texture('block/destroy_stage_6.png', 'environment/destroy_stage_6.png')
move_texture('block/destroy_stage_7.png', 'environment/destroy_stage_7.png')
move_texture('block/destroy_stage_8.png', 'environment/destroy_stage_8.png')
move_texture('block/destroy_stage_9.png', 'environment/destroy_stage_9.png')
move_texture('entity/arrow.png', 'entity/arrows.png')
move_texture('entity/snowman.png', 'entity/snow_golem.png')
move_texture('entity/cat/black.png', 'entity/cat/blackcat.png')
move_texture('entity/chest/normal_double.png', 'entity/chest/double_normal.png')
move_texture('entity/zombie_pigman.png', 'entity/pig/pigzombie.png')
move_texture('entity/rabbit/black.png', 'entity/rabbit/blackrabbit.png')
move_texture('entity/wither/', 'entity/wither_boss/')
move_texture('items/acacia_boat.png', 'items/boat_acacia.png')
move_texture('items/birch_boat.png', 'items/boat_birch.png')
move_texture('items/dark_oak_boat.png', 'items/boat_darkoak.png')
move_texture('items/jungle_boat.png', 'items/boat_jungle.png')
move_texture('items/oak_boat.png', 'items/boat_oak.png')
move_texture('items/spruce_boat.png', 'items/boat_spruce.png')
move_texture('items/clock_00.png', 'items/clock_item.png')
move_texture('items/compass_19.png', 'items/compass_item.png')
move_texture('items/fish_cod_cooked.png', 'items/fish_cooked.png')
move_texture('items/fish_cod_raw.png', 'items/fish_raw.png')
move_texture('items/beetroot_seeds.png', 'items/seeds_beetroot.png')
move_texture('models/armor/chainmail_layer_1.png', 'models/armor/chain_1.png')
move_texture('models/armor/chainmail_layer_2.png', 'models/armor/chain_2.png')
move_texture('models/armor/diamond_layer_1.png', 'models/armor/diamond_1.png')
move_texture('models/armor/diamond_layer_2.png', 'models/armor/diamond_2.png')
move_texture('models/armor/gold_layer_1.png', 'models/armor/gold_1.png')
move_texture('models/armor/gold_layer_2.png', 'models/armor/gold_2.png')
move_texture('models/armor/iron_layer_1.png', 'models/armor/iron_1.png')
move_texture('models/armor/iron_layer_2.png', 'models/armor/iron_2.png')
move_texture('painting/paintings_kristoffer_zetterstrand.png', 'painting/kz.png')

if os.path.isfile('blocks/lever.png'):
    shutil.copy2('blocks/lever.png', 'items/lever.png')

os.chdir('../..')

out_zip = zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED)
os.chdir(out_dir)

for root, dirs, files in os.walk('.'):
    for file in files:
        out_zip.write(os.path.join(root, file))

os.chdir('..')
out_zip.close()

shutil.rmtree(in_dir)
shutil.rmtree(out_dir)
