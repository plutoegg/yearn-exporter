
from brownie import chain, convert
from yearn import constants
from yearn.entities import TreasuryTx
from yearn.networks import Network
from yearn.partners.partners import partners
from yearn.treasury.accountant.classes import Filter, HashMatcher, IterFilter

hashes = {
    Network.Mainnet: {
        'thegraph': [
            '0x33a50699c95fa37e2cc4032719ed6064bbd892b0992dde01d4ef9b3470b9da0b',
        ],
        'yswap': [
            ['0xc66a60d1578ad80f9f1bfb29293bd9f8699c3d61b237a7cf8c443d00ffb3809e', Filter('from_address.nickname',"Disperse.app")],
            ['0xd45f5cf3388cea2a684ae124bac7bccb010442862cc491fdb4fc06d57c6aab5d', Filter('log_index',None)],
        ],
        'ychad': [
            ['0x1ba68f5f52b27e9b6676b952c08d29e2fe29f8ddffd7427911046915db5b4966', Filter('from_address.nickname',"Disperse.app")],
        ],
        'ymechs': [
            '0x1ab9ff3228cf25bf2a7c1eac596e836069f8c0adc46acd46d948eb77743fbb96',
            '0xe2a6bec23d0c73b35e969bc949072f8c1768767b06d57e5602b2b95eddf41a66',
        ],
        'ykeeper': [
            '0x1ab9ff3228cf25bf2a7c1eac596e836069f8c0adc46acd46d948eb77743fbb96',
            '0xe2a6bec23d0c73b35e969bc949072f8c1768767b06d57e5602b2b95eddf41a66',
        ],
    }
}.get(chain.id, {})

def is_partner_fees(tx: TreasuryTx) -> bool:
    if tx.from_address.address == constants.YCHAD_MULTISIG and tx.to_address:
        for partner in partners:
            if not (
                tx.to_address.address == convert.to_address(partner.treasury) or
                (hasattr(partner, 'retired_treasuries') and tx.to_address.address in partner.retired_treasuries)
            ):
                continue
            if any(tx.token.address.address == convert.to_address(wrapper.vault) for wrapper in partner.flat_wrappers):
                return True
    
    # DEV figure out why these weren't captured by the above
    hashes = {
        Network.Mainnet: [
            # Thought we automated these... why aren't they sorting successfully? 
            ["0x590b0cc67ba42dbc046b8cbfe2d314fbe8da82f11649ef21cdacc61bc9752d83", IterFilter('log_index',[275,276,278])],
            ["0xd1b925ad7fdd9abdd31460a346d081d6afe9f6cb1c1b0cd5f6129885edf318da", IterFilter('log_index',[174,177])],
            ["0xe11b4e3ece520c1818ffe821c038779f87c293aa32c26115265b6b8fb23c30bd", Filter('log_index', 154)],
        ],
    }.get(chain.id, [])

    if tx in HashMatcher(hashes):
        return True
    return False
